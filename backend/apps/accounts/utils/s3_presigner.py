import logging

import boto3
from django.conf import settings

logger = logging.getLogger(__name__)
def generate_presigned_url(user_id: int, filename: str, content_type: str)-> str:
    """Generate a presigned URL for uploading a file to S3.

    Args:
        user_id (int): User ID for whom the file is being uploaded.
        filename (str): The name of the file to be uploaded.
        content_type (str): The content type of the file being uploaded. for rejecting files with wrong content type

    Returns:
        str: A presigned URL of S3
    """
    try:
        s3 = boto3.client("s3", region_name=settings.AWS_REGION)
        key = f"user_uploads/{user_id}/{filename}"
        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": settings.AWS_S3_PROFILE_BUCKET,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=600,
        )
        return url, key
    except Exception as e:
        logger.error(f"Failed to generate presigned URL: {str(e)}")
        raise
    