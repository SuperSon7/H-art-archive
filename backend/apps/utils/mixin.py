import logging
from uuid import uuid4

from botocore.exceptions import ClientError
from django.conf import settings

from apps.utils.s3_presigner import create_presigned_url

logger = logging.getLogger(__name__)


class PresignedUploadMixin:
    PRESIGNED_EXPIRES = settings.AWS_PRESIGNED_EXPIRES


def _build_s3_key(self, category: str, object_id: int, ext: str, subdir: str | None = None) -> str:
    """Generate an S3 key for a given category/object."""
    filename = f"{uuid4().hex}{ext}"
    parts = [category, str(object_id)]
    if subdir:
        parts.append(subdir)
    parts.append(filename)
    return "/".join(parts)


def get_presigned_url(self, *, bucket: str, key: str, content_type: str) -> tuple[str, str]:
    try:
        url, k = create_presigned_url(
            bucket=bucket, key=key, content_type=content_type, expires=self.PRESIGNED_EXPIRES
        )
        return url, k
    except ClientError as e:
        logger.error(f"S3 ClientError: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
