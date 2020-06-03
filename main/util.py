import os

import boto3

from nitro_labs import settings


def generate_aws_url(key) -> str:
    client = connect_to_s3().meta.client
    return client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": os.path.join(key.storage.location, key.name),
            'ResponseContentType': 'image/jpeg'
        },
        ExpiresIn=1000
    )


def connect_to_s3():
    aws_kwargs = {
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY
    }
    return boto3.resource("s3", **aws_kwargs)
