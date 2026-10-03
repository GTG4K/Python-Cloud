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

if __name__ == "__main__":
    s3_client = init_client()
