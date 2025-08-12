import logging

from django.conf import settings

from .s3_client import get_s3_client

logger = logging.getLogger(__name__)


def s3_key_for_user_upload(user_id: int, filename: str) -> str:
    return f"user_uploads/{user_id}/{filename}"


def generate_presigned_url(user_id: int, filename: str, content_type: str) -> tuple[str, str]:
    """Generate a presigned URL for uploading a file to S3.

    Args:
        user_id (int): User ID for whom the file is being uploaded.
        filename (str): The name of the file to be uploaded.
        content_type (str): The content type of the file being uploaded. for rejecting files with wrong content type

    Returns:
        str: A presigned URL of S3
    """
    s3 = get_s3_client()
    key = s3_key_for_user_upload(user_id, filename)
    try:
        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": settings.AWS_S3_BUCKET_NAME,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=settings.AWS_PRESIGNED_EXPIRES,
        )
        return url, key
    except Exception as e:
        logger.error(f"Failed to generate presigned URL: {str(e)}")
        raise
