import logging
import os
from uuid import uuid4

import boto3
import httpx
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile

from app.core.config import settings

logger = logging.getLogger(__name__)


def upload_file(f: UploadFile):
    if not f.filename:
        raise HTTPException(status_code=400, detail="File is required")

    _, ext = os.path.splitext(f.filename)
    key = f"images/{uuid4()}{ext}"
    presigned_url = _generate_presigned_url(key)
    response = httpx.put(presigned_url, files={"file": f.file})
    if response.status_code != 200:
        logger.error(response.text)
        raise HTTPException(status_code=500, detail="Failed to upload profile image")

    return f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{key}"


def _generate_presigned_url(key: str):
    s3_client = boto3.client("s3")
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": settings.AWS_S3_BUCKET_NAME, "Key": key},
            ExpiresIn=600,  # 10 minutes
        )
    except ClientError:
        raise
    return url
