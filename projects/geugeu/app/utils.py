import logging
from typing import Literal

import boto3
from botocore.exceptions import ClientError

from app.config import settings

logger = logging.getLogger(__name__)


def create_presigned_url(
    method: Literal["get_object", "put_object"], key: str, expiration: int = 300
) -> str | None:
    s3_client = boto3.client("s3")
    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod=method,
            Params={"Bucket": settings.S3_BUCKET_NAME, "Key": key},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logger.error(e)
        return None

    return presigned_url
