import boto3


def download_data(bucket, s3_path, local_path):
    s3 = boto3.resource("s3")
    s3.Bucket(bucket).download_file(s3_path, local_path)


def upload_data(bucket, s3_path, local_path):
    s3 = boto3.resource("s3")

    s3.Bucket(bucket).upload_file(local_path, s3_path)
