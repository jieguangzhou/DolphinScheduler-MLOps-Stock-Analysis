import boto3


def download_data(bucket, s3_path, local_path):
    s3 = boto3.resource("s3")
    s3.Bucket(bucket).download_file(s3_path, local_path)


def download_data_without_bucket(s3_path, local_path):
    path = s3_path.replace("s3://", "")
    (bucket, key) = path.split("/", 1)
    download_data(bucket, key, local_path)


def upload_data(bucket, s3_path, local_path):
    s3 = boto3.resource("s3")
    s3.Bucket(bucket).upload_file(local_path, s3_path)
