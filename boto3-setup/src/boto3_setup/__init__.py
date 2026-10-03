import io
import logging
from hashlib import md5
from os import getenv
from time import localtime
from urllib.request import urlopen
from uuid import uuid4

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


def delete_bucket(aws_s3_client, bucket_name):
    if aws_s3_client is None:
        return False

    try:
        aws_s3_client.delete_bucket(Bucket=bucket_name)
    except ClientError as error:
        logging.error(error)
        return False

    return True


def bucket_exists(aws_s3_client, bucket_name):
    if aws_s3_client is None:
        return False

    try:
        response = aws_s3_client.head_bucket(Bucket=bucket_name)
    except ClientError as error:
        logging.error(error)
        return False

    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True

    return False


def download_file_and_upload_to_s3(
    aws_s3_client,
    bucket_name,
    url,
    file_name,
    keep_local=False,
):
    if aws_s3_client is None:
        return False

    with urlopen(url) as response:
        content = response.read()

    try:
        aws_s3_client.upload_fileobj(
            Fileobj=io.BytesIO(content),
            Bucket=bucket_name,
            Key=file_name,
        )
    except Exception as error:
        logging.error(error)
        return False

    if keep_local:
        with open(file_name, mode="wb") as image_file:
            image_file.write(content)

    region = getenv("aws_region")
    if region == "us-east-1":
        return f"https://s3.amazonaws.com/{bucket_name}/{file_name}"

    return f"https://s3-{region}.amazonaws.com/{bucket_name}/{file_name}"


def set_object_access_policy(aws_s3_client, bucket_name, file_name):
    if aws_s3_client is None:
        return False

    try:
        response = aws_s3_client.put_object_acl(
            ACL="public-read",
            Bucket=bucket_name,
            Key=file_name,
        )
    except ClientError as error:
        logging.error(error)
        return False

    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True

    return False


if __name__ == "__main__":
    s3_client = init_client()
    region = getenv("aws_region")

    bucket_name = f"boto3-setup-{uuid4().hex[:8]}"
    print(f"created bucket status: {create_bucket(s3_client, bucket_name, region)}")
    print(f"Bucket exists: {bucket_exists(s3_client, bucket_name)}")

    file_name = f"image_file_{md5(str(localtime()).encode('utf-8')).hexdigest()}.jpg"

    # funny crow
    image_url = "https://thumbs.dreamstime.com/b/crow-standing-bench-iage-corvus-surrey-england-326402189.jpg"

    print(
        download_file_and_upload_to_s3(
            s3_client,
            bucket_name,
            image_url,
            file_name,
            keep_local=True,
        )
    )

    print(
        f"set read status: {set_object_access_policy(s3_client, bucket_name, file_name)}"
    )

    buckets = list_buckets(s3_client)

    if buckets:
        for bucket in buckets["Buckets"]:
            print(f" {bucket['Name']}")
