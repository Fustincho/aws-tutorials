# Sagemaker Pipelines

## Introduction

This repository offers a comprehensive guide on AWS Sagemaker Pipelines, structured to facilitate both novice and experienced users in understanding and implementing Sagemaker Pipelines. The approach is incremental, beginning with fundamental concepts and progressively moving towards more complex pipeline applications.

## Objective

The goal of this tutorial is to provide practical examples and clear explanations for creating and managing machine learning pipelines using AWS Sagemaker. Upon completion, learners will have gained a thorough understanding of Sagemaker Pipelines, equipping them with the skills to implement these in various machine learning projects.

## Structure

The content is organized into a series of Jupyter notebooks, each dedicated to a specific aspect of Sagemaker Pipelines. The material is segmented into units, with each subsequent unit expanding upon the knowledge and skills presented in the preceding ones.

### Units Overview

1. [Your first Sagemaker Endpoint](unit_1.ipynb): This unit introduces the foundational steps to create and deploy a machine learning model using AWS Sagemaker. The primary focus is on setting up a basic Sagemaker endpoint, which serves as a critical component for model hosting and real-time predictions.

1.1. *(Optional)* [Improving Efficiency with SageMaker Warm Pools](optional_1.ipynb): This unit demonstrates how to use SageMaker Warm Pools to reduce the startup time and improve the efficiency of training jobs. We will build on previous units by reusing the training job structure and data, adding the warm pool feature, and training multiple models with varying hyperparameters to observe the reduced training time.

2. [Automating Workflows with SageMaker Pipelines](unit_2.ipynb): Learn to create and manage automated workflows for machine learning models using SageMaker Pipelines. We'll build on Unit 1 by reloading essential components, initializing the SageMaker session, and using the XGBoost Docker image for consistency.

3. [Enhancing Models with Hyperparameter Tuning](unit_3.ipynb): Discover how to improve your model's accuracy with SageMaker's Hyperparameter Tuning. This unit focuses on fine-tuning model settings and integrating these optimizations into your pipelines for seamless automation.

## Prerequisites

- Understanding of Python and foundational machine learning concepts.
- Access to an AWS account and basic knowledge of AWS services.
- Familiarity with Jupyter notebooks.
- You need to run these notebooks within a SageMaker service (e.g., Studio, Studio Classic, Notebook instance). Ensure that this service has an AWS Identity and Access Management (IAM) role with the necessary permissions for Amazon SageMaker to access resources such as S3 buckets, execute training jobs, and deploy models. Here’s an example of a basic policy:

```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket",
                    "s3:DeleteObject"
                ],
                "Resource": [
                    "arn:aws:s3:::your-s3-bucket/*",
                    "arn:aws:s3:::your-s3-bucket"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "sagemaker:CreateModel",
                    "sagemaker:CreateEndpointConfig",
                    "sagemaker:CreateEndpoint",
                    "sagemaker:DeleteEndpoint",
                    "sagemaker:DeleteEndpointConfig"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "sagemaker:CreateTrainingJob",
                    "sagemaker:DescribeTrainingJob",
                    "sagemaker:StopTrainingJob"
                ],
                "Resource": "*"
            }
        ]
    }
```

## Getting Started

To start, clone this repository and navigate to the respective notebook directories. Each notebook is equipped with comprehensive instructions and explanations, guiding through each pipeline component.

## Contributing

Contributions are welcome. Interested contributors are encouraged to fork the repository and submit pull requests with suggested changes or enhancements.

---

Wishing all learners a productive and enlightening experience.

Fustincho
