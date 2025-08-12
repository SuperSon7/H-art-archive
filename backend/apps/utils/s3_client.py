import boto3
from botocore.client import Config
from django.conf import settings


def get_s3_client():
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
