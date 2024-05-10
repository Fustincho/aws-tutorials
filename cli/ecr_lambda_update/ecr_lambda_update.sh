#!/bin/bash

# Create a custom log message
ECHO_PREFIX="[INFO] - "
log_message() {
  echo "$ECHO_PREFIX$1"
}

# Exit immediately if a command exits with a non-zero status
set -e

# Parameter default values
ECR_REPO_NAME=""
LAMBDA_FUNCTION_NAME=""
IMAGE_NAME="latest"
AWS_REGION="us-east-1"

# Parse command-line arguments
while getopts ":r:l:i:g:" opt; do
  case $opt in
    r)
      ECR_REPO_NAME="$OPTARG"
      ;;
    l)
      LAMBDA_FUNCTION_NAME="$OPTARG"
      ;;
    i)
      IMAGE_NAME="$OPTARG"
      ;;
    g)
      AWS_REGION="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Check if both the ECR repository name and Lambda function name are provided
if [ -z "$ECR_REPO_NAME" ] || [ -z "$LAMBDA_FUNCTION_NAME" ]; then
  echo "Please provide both the ECR repository name (-r) and the Lambda function name (-l)."
  exit 1
fi

# Fetch ECR repository URI based on the repository name
ECR_REPO_URI=$(aws --no-cli-pager ecr describe-repositories --repository-names $ECR_REPO_NAME --region $AWS_REGION | jq -r '.repositories[0].repositoryUri')

# Check if the repository exists
if [ -z "$ECR_REPO_URI" ]; then
  echo "ECR repository '$ECR_REPO_NAME' not found in region '$AWS_REGION'."
  exit 1
fi

docker build -t my-image:$IMAGE_NAME .
docker tag my-image:$IMAGE_NAME $ECR_REPO_URI:$IMAGE_NAME

# AWS ECR login (this will authenticate Docker with your ECR registry)
log_message "Logging in ECR"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URI

docker push $ECR_REPO_URI:$IMAGE_NAME

log_message "Image pushed to $ECR_REPO_NAME:$IMAGE_NAME successfully."

###### TRACK THE UPDATE STATUS

log_message "Updating $LAMBDA_FUNCTION_NAME:"
# Update Lambda function code with the new Docker image
aws  --no-cli-pager lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --image-uri $ECR_REPO_URI:$IMAGE_NAME --region $AWS_REGION

# Initialize the last update status variable
LAST_UPDATE_STATUS="InProgress"

# Initialize the progress dots
PROGRESS_MESSAGE="Update in progress"
PROGRESS_DOTS=""

# Loop while the update is still in progress
while [ "$LAST_UPDATE_STATUS" == "InProgress" ]; do
    # Retrieve the last update status of the Lambda function
    LAST_UPDATE_STATUS=$(aws lambda get-function \
        --function-name "$LAMBDA_FUNCTION_NAME" \
        --query 'Configuration.LastUpdateStatus' \
        --output text)

    # Append a dot to the progress message
    PROGRESS_DOTS+="."

    # Print the current progress message
    echo -ne "$PROGRESS_MESSAGE$PROGRESS_DOTS\r"

    # If still in progress, sleep before retrying
    if [ "$LAST_UPDATE_STATUS" == "InProgress" ]; then
        sleep 1
    fi
done

# Determine the final status
if [ "$LAST_UPDATE_STATUS" == "Successful" ]; then
    echo -e "$PROGRESS_MESSAGE${PROGRESS_DOTS}!"
else
    echo -e "$PROGRESS_MESSAGE${PROGRESS_DOTS}X\nLambda function update failed. Status: $LAST_UPDATE_STATUS"
    exit 1
fi

echo "The Lambda function '$LAMBDA_FUNCTION_NAME' ($AWS_REGION) was successfully updated with the image: $ECR_REPO_NAME:$IMAGE_NAME"
