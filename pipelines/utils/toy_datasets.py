import pandas as pd
import os
from sklearn import datasets
from sklearn.model_selection import train_test_split
import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(file_name, bucket, prefix, object_name=None):

    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(file_name,
                                         bucket,
                                         f'{prefix}/{object_name}')
    except NoCredentialsError:
        print('Credentials not available')
    except Exception as e:
        print(f'Error uploading file to S3: {e}')


def upload_dataset_to_s3(dataset_name, bucket_name, cleanup=True):

    dataset = getattr(datasets, f"load_{dataset_name}")()
    data = pd.DataFrame(data=dataset['data'], columns=dataset['feature_names'])
    data.insert(0, 'target', dataset['target'])

    train_data, test_data = train_test_split(data,
                                             test_size=0.2,
                                             random_state=101)

    train_data.to_csv('train_data.csv', index=False)
    test_data.to_csv('test_data.csv', index=False)

    prefix = f'{dataset_name}_dataset'

    upload_to_s3('train_data.csv', bucket_name, prefix, 'train_data.csv')
    upload_to_s3('test_data.csv', bucket_name, prefix, 'test_data.csv')

    print('Files uploaded to S3 successfully.')

    if cleanup is True:
        # Delete local files after uploading to S3
        os.remove('train_data.csv')
        os.remove('test_data.csv')
        print('Cleanup complete!')

