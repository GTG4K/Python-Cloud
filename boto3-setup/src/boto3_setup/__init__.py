import logging
from os import getenv

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()


def init_client():
    try:
        client = boto3.client(
            "s3",
            aws_access_key_id=getenv("aws_access_key_id"),
            aws_secret_access_key=getenv("aws_secret_access_key"),
            aws_session_token=getenv("aws_session_token"),
            region_name=getenv("aws_region"),
        )
        client.list_buckets()
    except ClientError as error:
        logging.error(error)
        return None
    except Exception:
        logging.error("Unexpected error")
        return None

    return client


def list_buckets(aws_s3_client):
    if aws_s3_client is None:
        return False

    try:
        return aws_s3_client.list_buckets()
    except ClientError as error:
        logging.error(error)
        return False


def create_bucket(aws_s3_client, bucket_name, region="us-east-1"):
    if aws_s3_client is None:
        return False

    try:
        if region == "us-east-1":
            aws_s3_client.create_bucket(Bucket=bucket_name)
        else:
            aws_s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
    except ClientError as error:
        logging.error(error)
        return False

    return True


if __name__ == "__main__":
    s3_client = init_client()
    region = getenv("aws_region")

    print(f"created bucket status: {create_bucket(s3_client, 'new-bucket-btu', region)}")
    buckets = list_buckets(s3_client)

    if buckets:
        for bucket in buckets["Buckets"]:
            print(f" {bucket['Name']}")
