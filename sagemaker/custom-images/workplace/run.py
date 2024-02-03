import json
import os
import subprocess
import sys

import boto3
import sagemaker
import yaml

# Load the configuration file
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Access configuration values
REPO_NAME = config['REPO_NAME']
IMAGE_NAME = config['IMAGE_NAME']
DOMAIN_NAME = config['DOMAIN_NAME']
UPDATE = config['UPDATE']
DISPLAY_NAME = config['DISPLAY_NAME']
IMAGE_DESCRIPTION = config['IMAGE_DESCRIPTION']
DOCKERFILE_TEMPLATE = config['DOCKERFILE_TEMPLATE']

sm = boto3.client("sagemaker")

domains = [d for d in sm.list_domains()["Domains"] if d["Status"]
           == 'InService']

try:
    # Attempt to find the desired domain without a default value for `next`
    desired_domain = next(
        domain for domain in domains if domain['DomainName'] == DOMAIN_NAME)
    domain_id = desired_domain['DomainId']
    print(f"Found domain: {DOMAIN_NAME}. DomainId: {domain_id}")
except StopIteration as exc:
    # Raise an exception if the domain is not found
    raise Exception(f"Domain with name '{DOMAIN_NAME}' not found.") from exc


with open('Dockerfile', 'w') as dockerfile:
    dockerfile.write(DOCKERFILE_TEMPLATE)

print("[BEGIN] Creating and uploading image to ECR")
return_code = subprocess.call(
    ['./build_image.sh', '-r', REPO_NAME, '-i', IMAGE_NAME])

if return_code != 0:
    print("[FAILURE] Creating and uploading image to ECR")
    sys.exit(1)

print("[SUCCESS] Creating and uploading image to ECR")


app_image_config_name = f"{IMAGE_NAME}-config"

# Define the JSON data as a Python dictionary
app_image_config = {
    "AppImageConfigName": app_image_config_name,
    "KernelGatewayImageConfig": {
        "KernelSpecs": [
            {
                "Name": "env1",
                "DisplayName": DISPLAY_NAME
            }
        ],
        "FileSystemConfig": {
            "MountPath": "/root",
            "DefaultUid": 0,
            "DefaultGid": 0
        }
    }
}

role = sagemaker.get_execution_role()

NOTEBOOK_METADATA_FILE = "/opt/ml/metadata/resource-metadata.json"

if os.path.exists(NOTEBOOK_METADATA_FILE):
    with open(NOTEBOOK_METADATA_FILE, "rb") as f:
        md = json.loads(f.read())

account_id = boto3.client("sts").get_caller_identity()["Account"]
region = md["ResourceArn"].split(":")[3]
full_name = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{REPO_NAME}:{IMAGE_NAME}"

if UPDATE:
    print("[BEGIN] - Updating Image Version")
    r = sm.create_image_version(
        BaseImage=full_name,
        ImageName=IMAGE_NAME,
    )
    print("[SUCCESS] - Updating Image Version")
    print(r)
    sys.exit()

print(f"[BEGIN] - Creating Image in Domain {DOMAIN_NAME}")

r = sm.create_image(
    Description=IMAGE_DESCRIPTION,
    DisplayName=DISPLAY_NAME,
    ImageName=IMAGE_NAME,
    RoleArn=role,
)

print("Image created!")
print(r)

def create_image_version_with_retry(sagemaker_client, base_image, image_name, max_retries=3, initial_wait_time=10):
    """
    Attempts to create an image version in AWS SageMaker, with retry logic for handling 'ResourceInUse' errors.
    
    This retry mechanism is implemented because the 'ResourceInUse' error may occur if the image is still being created.
    The function uses an exponential backoff strategy for retries, doubling the wait time after each retry.
    
    Parameters:
    - sagemaker_client: The boto3 SageMaker client instance to use for making the API call.
    - base_image: The URI of the Docker image in Amazon ECR that is to be used as the base image for the SageMaker image version.
    - image_name: The name of the SageMaker image to which the version is added.
    - max_retries: The maximum number of retry attempts (default is 3).
    - initial_wait_time: The initial wait time (in seconds) before the first retry attempt (default is 10 seconds).
    
    Returns:
    - The response from the `create_image_version` API call if successful.
    
    Raises:
    - Exception: If the maximum number of retries is reached without success.
    - ClientError: If an AWS error occurs that is not 'ResourceInUse'.
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = sagemaker_client.create_image_version(
                BaseImage=base_image,
                ImageName=image_name,
            )
            print("Image version created successfully!")
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUse':
                print(f"Resource in use, retrying in {initial_wait_time} seconds...")
                time.sleep(initial_wait_time)
                # Increase the wait time for the next retry
                initial_wait_time *= 2
                retry_count += 1
            else:
                # If the error is not 'ResourceInUse', re-raise the exception
                raise
    raise Exception("Max retries reached. Image version creation failed.")

try:
    r = create_image_version_with_retry(sm, full_name, IMAGE_NAME)
    print(r)
except Exception as e:
    print(f"Failed to create image version: {e}")
    print(f"[FAILURE] - Creating Image in Domain: {DOMAIN_NAME}")

# create image config
r = sm.create_app_image_config(
    AppImageConfigName=app_image_config["AppImageConfigName"],
    KernelGatewayImageConfig=app_image_config["KernelGatewayImageConfig"],
)

print("App image config created!")
print(r)

update_domain_config = {
    "DefaultUserSettings": {
        "KernelGatewayAppSettings": {
            "CustomImages": [
                {
                    "ImageName": IMAGE_NAME,
                    "AppImageConfigName": app_image_config_name
                }
            ]
        }
    }
}

r = sm.update_domain(
    DomainId=domain_id,
    DefaultUserSettings=update_domain_config["DefaultUserSettings"],
)

print("Domain updated successfully!")
print(r)
print(f"[SUCCESS] - Creating Image in Domain: {DOMAIN_NAME}")
