from unittest.mock import Mock, patch

import boto3
import pytest
from moto import mock_aws

from apps.accounts.oauth import login_with_social
from apps.utils.s3_presigner import generate_presigned_url


@pytest.mark.unit
class TestGeneratePresignedUrl:
    @mock_aws
    def test_generate_presigned_url_success(self):
        """S3 presigned URL 생성 성공 테스트"""
        # Mock S3 bucket 생성
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")

        with (
            patch("django.conf.settings.AWS_S3_PROFILE_BUCKET", "test-bucket"),
            patch("django.conf.settings.AWS_REGION", "us-east-1"),
        ):
            url, key = generate_presigned_url(
                user_id=1, filename="test.jpg", content_type="image/jpeg"
            )

            assert url is not None
            assert key == "user_uploads/1/test.jpg"

    @patch("boto3.client")
    def test_generate_presigned_url_failure(self, mock_boto3):
        """S3 presigned URL 생성 실패 테스트"""
        mock_client = Mock()
        mock_client.generate_presigned_url.side_effect = Exception("S3 error")
        mock_boto3.return_value = mock_client

        with pytest.raises(Exception):
            generate_presigned_url(1, "test.jpg", "image/jpeg")


@pytest.mark.unit
@pytest.mark.django_db
class TestLoginWithSocial:
    @patch("apps.accounts.oauth.SocialAdapterRegistry.get_adapter")
    def test_successful_social_login_new_user(self, mock_get_adapter):
        """새 사용자 소셜 로그인 성공 테스트"""
        # Mock adapter 설정
        mock_adapter = Mock()
        mock_adapter.exchange_code_for_token.return_value = "access_token"
        mock_adapter.get_user_info.return_value = {"id": "123", "email": "new@example.com"}
        mock_adapter.normalize_user_data.return_value = {
            "provider": "google",
            "social_id": "123",
            "email": "new@example.com",
        }
        mock_get_adapter.return_value = mock_adapter

        result = login_with_social("google", "auth_code", "redirect_uri")

        assert "access" in result
        assert "refresh" in result
        assert "user_type" in result

    @patch("apps.accounts.oauth.SocialAdapterRegistry.get_adapter")
    def test_social_login_existing_user(self, mock_get_adapter, social_user):
        """기존 사용자 소셜 로그인 테스트"""
        mock_adapter = Mock()
        mock_adapter.exchange_code_for_token.return_value = "access_token"
        mock_adapter.get_user_info.return_value = {"id": "123456789", "email": "social@example.com"}
        mock_adapter.normalize_user_data.return_value = {
            "provider": "google",
            "social_id": "123456789",
            "email": "social@example.com",
        }
        mock_get_adapter.return_value = mock_adapter

        result = login_with_social("google", "auth_code", "redirect_uri")

        assert "access" in result
        assert result["user_type"] == "collector"

    @patch("apps.accounts.oauth.SocialAdapterRegistry.get_adapter")
    def test_social_login_adapter_error(self, mock_get_adapter):
        """소셜 로그인 어댑터 오류 테스트"""
        mock_adapter = Mock()
        mock_adapter.exchange_code_for_token.side_effect = Exception("OAuth error")
        mock_get_adapter.return_value = mock_adapter

        with pytest.raises(Exception):
            login_with_social("google", "invalid_code", "redirect_uri")
