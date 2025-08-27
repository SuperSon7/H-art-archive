import logging
from uuid import uuid4

from django.conf import settings

from .s3_client import get_s3_client

logger = logging.getLogger(__name__)


def s3_key_for_upload(category: str, object_id: int, ext: str, subdir: str | None = None) -> str:
    """Generate an S3 key for a given category/object."""
    filename = f"{uuid4().hex}{ext}"
    parts = [category, str(object_id)]
    if subdir:
        parts.append(subdir)
    parts.append(filename)
    return "/".join(parts)


# boto의 generate_presigned_url 과 혼동 방지를 위해 create_presigned_url 로 변경
def create_presigned_url(
    bucket: str, key: str, content_type: str, expires: int | None = None
) -> tuple[str, str]:
    """Generate a presigned URL for uploading a file to S3.

    Args:
        user_id (int): User ID for whom the file is being uploaded.
        filename (str): The name of the file to be uploaded.
        content_type (str): The content type of the file being uploaded. for rejecting files with wrong content type

    Returns:
        str: A presigned URL of S3
    """
    s3 = get_s3_client()
    try:
        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": bucket,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=expires or settings.AWS_PRESIGNED_EXPIRES,
        )
        return url, key
    except Exception as e:
        logger.error(f"Failed to generate presigned URL: {str(e)}")
        raise
