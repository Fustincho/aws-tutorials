#!/bin/bash

# Initialize variables
REPO_NAME=""
IMAGE_NAME=""

# Parse script arguments for -r (REPO_NAME) and -i (IMAGE_NAME)
while getopts ":r:i:" opt; do
  case ${opt} in
    r )
      REPO_NAME=$OPTARG
      ;;
    i )
      IMAGE_NAME=$OPTARG
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      exit 1
      ;;
  esac
done

# Check if REPO_NAME and IMAGE_NAME were provided
if [ -z "$REPO_NAME" ] || [ -z "$IMAGE_NAME" ]; then
    echo "Both -r (REPO_NAME) and -i (IMAGE_NAME) arguments are required."
    exit 1
fi

# Region, defaults to us-east-1
REGION=$(aws configure get region)
REGION=${REGION:-us-east-1}

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
FULL_NAME="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${IMAGE_NAME}"

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${REPO_NAME}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${REPO_NAME}" > /dev/null
fi

# Login to ECR
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${FULL_NAME}

# Build and push the image
docker build . -t ${IMAGE_NAME} -t ${FULL_NAME}

docker push ${FULL_NAME}
