import logging
from uuid import uuid4

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger(__name__)


class PresignedUploadMixin:
    PRESIGNED_EXPIRES = settings.AWS_PRESIGNED_EXPIRES

    def _get_s3_client(self):
        cfg = Config(
            signature_version="s3v4",  # 권장 서명 버전
            s3={"addressing_style": "path"},  # LocalStack 호환성 ↑
        )
        return boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            endpoint_url=settings.AWS_ENDPOINT or None,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=cfg,
        )

    def _build_s3_key(
        self, category: str, object_id: int, ext: str, subdir: str | None = None
    ) -> str:
        """Generate an S3 key for a given category/object.
        URL like
        - artworks/1/images/1/1234567890.jpg
        """
        filename = f"{uuid4().hex}{ext}"
        parts = [category, str(object_id)]
        if subdir:
            parts.append(subdir)
        parts.append(filename)
        return "/".join(parts)

    def _get_presigned_url(
        self, *, bucket: str, key: str, content_type: str, expires: int | None = None
    ) -> tuple[str, str]:
        """Generate a presigned URL for uploading a file to S3.
        Args:
            user_id (int): User ID for whom the file is being uploaded.
            filename (str): The name of the file to be uploaded.
            content_type (str): The content type of the file being uploaded. for rejecting files with wrong content type
        Returns:
            str: A presigned URL of S3
        """
        s3 = self._get_s3_client()
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
        except ClientError as e:
            logger.error(f"S3 ClientError: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to generate presigned URL: {str(e)}")
            raise
