#!/bin/bash

# Default values
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

# Docker build and tag
docker build -t my-image:$IMAGE_NAME .
docker tag my-image:$IMAGE_NAME $ECR_REPO_URI:$IMAGE_NAME

# AWS ECR login (this will authenticate Docker with your ECR registry)
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URI

# Docker push
docker push $ECR_REPO_URI:$IMAGE_NAME

echo "Image pushed to ECR successfully."

# Update Lambda function code with the new Docker image
aws  --no-cli-pager lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --image-uri $ECR_REPO_URI:$IMAGE_NAME --region $AWS_REGION

echo "Lambda function '$LAMBDA_FUNCTION_NAME' updated with the new Docker image ('$IMAGE_NAME') in region '$AWS_REGION'."
