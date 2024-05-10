# ECR Image Push and Lambda Update Script

This script automates the process of pushing a Docker image to [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/) and updating an [AWS Lambda](https://aws.amazon.com/lambda/) function with the latest image. It accepts the ECR repository name and Lambda function name as command-line arguments, dynamically fetches the ECR repository URI, builds, tags, and pushes the Docker image to ECR, and finally updates the Lambda function with the new Docker image.

## Requirements

To run this script you require an user with permissions specified in the following policy to function correctly. The policy grants access to read and push images to a private Amazon ECR repository, as well as update and fetch Lambda function code and configurations:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability",
                "ecr:DescribeRepositories",
                "ecr:DescribeImages",
                "ecr:ListTagsForResource",
                "ecr:DescribeImageScanFindings",
                "ecr:PutImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:GetAuthorizationToken"
            ],
            "Resource": "arn:aws:ecr:your-region:your-account-id:repository/your-repository-name"
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:UpdateFunctionCode",
                "lambda:GetFunction",
                "lambda:GetFunctionConfiguration"
            ],
            "Resource": "arn:aws:lambda:region:account-id:function:function-name"
        }
    ]
}
```

## How to Use

The script has four parameters:

- ECR_REPO_NAME (-r): The name of the Amazon ECR repository where Docker images are managed. **This parameter is required**.
- LAMBDA_FUNCTION_NAME (-l): The name of the AWS Lambda function to be updated. **This parameter is required**.
- IMAGE_NAME (-i): The tag or version of the Docker image to use. Defaults to "latest" if not specified.
- AWS_REGION (-g): The AWS region where both the ECR repository and the Lambda function are located. Defaults to "us-east-1" if not specified.

**Optional:** open the `ecr_lambda_update.sh` file and edit the default values.

### Make the Script Executable

```bash
chmod +x ecr_lambda_update.sh
```

Then you can run the script. Here's an example:

```bash
./ecr_lambda_update.sh -r your-ecr-repo -l your-lambda-function -i custom-image-name
```

Replace `your-ecr-repo` and `your-lambda-function` with the actual names of your ECR repository and Lambda function.

### Making the Script a Global Function

If you want to use the script globally from any folder, move the script to a global location and make it executable:

```bash
sudo mv ecr_lambda_update.sh /usr/local/bin/ecr_lambda_update
sudo chmod +x /usr/local/bin/ecr_lambda_update
```

### Set the `man` page

By default, manual pages are stored in system-wide directories. If you want to organize or keep your custom manual pages separate, you can create a personal directory for them.

#### 1. Create a Personal Manual Page Directory

```bash
mkdir -p ~/.local/share/man/man1/
```

This command creates the directory structure `~/.local/share/man/man1/` where you can store your custom manual pages. The `-p` option ensures that parent directories are created as needed.

#### 2. Add the Personal Manual Page Directory to MANPATH

To include your personal manual page directory in the `MANPATH`, add the following line to your shell configuration file (`~/.zshrc` for Zsh, `~/.bash_profile` for Bash):

```bash
export MANPATH="$HOME/.local/share/man:$MANPATH"
```

This line ensures that your custom manual pages are considered when searching for manuals.

#### 3. Restart Your Shell or Source the Configuration File

After adding the line to your shell configuration file, restart your shell or source the configuration file:

```bash
source ~/.zshrc   # For Zsh
source ~/.bash_profile   # For Bash
```

Alternatively, open a new terminal window for the changes to take effect.
