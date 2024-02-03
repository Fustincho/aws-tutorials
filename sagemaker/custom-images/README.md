# Introduction to Uploading Custom Images to Amazon SageMaker Using Python

## Overview

These notebooks are designed to provide you with a step-by-step approach to building, customizing, and deploying Docker images specifically tailored for use with Amazon SageMaker.

## Part 1: Building and Pushing Custom Docker Images to Amazon ECR

In the first part, [create_image.ipynb](https://github.com/Fustincho/aws-samples/blob/main/custom-images/create_image.ipynb), 
focuses on the process of creating a custom Docker image. This will involve selecting a base image, installing necessary dependencies, and configuring the environment to suit your specific ML requirements. Afterwards the notebook outlines the process of pushing this custom image to Amazon Elastic Container Registry (ECR).

## Part 2: Uploading and Using Custom Images in Amazon SageMaker Studio

In the second part, [update_domain.ipynb](https://github.com/Fustincho/aws-samples/blob/main/custom-images/update_domain.ipynb), 
focuses on integrating the custom Docker image with an Amazon SageMaker Domain. 

By the end of these notebooks, you will have a solid understanding of how to leverage the power of custom Docker images in Amazon SageMaker Studio, enabling you to tailor your ML model environments to your specific needs.