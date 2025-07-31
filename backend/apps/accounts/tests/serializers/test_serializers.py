# test_serializers.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from apps.accounts.serializers import LoginSerializer, ProfileImageUploadSerializer, SocialLoginSerializer

User = get_user_model()
@pytest.mark.django_db
class TestLoginSerializer:
    
    def test_valid_login_data(self, active_user):
        """유효한 로그인 데이터 테스트"""
        data = {
            'email': 'active@example.com',
            'password': 'testuser123'
        }
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        assert 'user' in serializer.validated_data
    
    def test_invalid_email(self):
        """잘못된 이메일 형식 테스트"""
        data = {
            'email': 'invalid-email',
            'password': 'test123'
        }
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors
    
    def test_short_password(self):
        """짧은 비밀번호 테스트"""
        data = {
            'email': 'test@example.com',
            'password': '123'
        }
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
    
    def test_invalid_credentials(self):
        """잘못된 인증 정보 테스트"""
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }
        serializer = LoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors

class TestProfileImageUploadSerializer:
    
    def test_valid_image_data(self):
        """유효한 이미지 업로드 데이터 테스트"""
        data = {
            'filename': 'profile.jpg',
            'content_type': 'image/jpeg'
        }
        serializer = ProfileImageUploadSerializer(data=data)
        assert serializer.is_valid()
    
    def test_invalid_content_type(self):
        """잘못된 content type 테스트"""
        data = {
            'filename': 'profile.pdf',
            'content_type': 'application/pdf'
        }
        serializer = ProfileImageUploadSerializer(data=data)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors
    
    def test_mismatched_extension_and_content_type(self):
        """확장자와 content type 불일치 테스트"""
        data = {
            'filename': 'profile.jpg',
            'content_type': 'image/png'
        }
        serializer = ProfileImageUploadSerializer(data=data)
        assert not serializer.is_valid()
    
    def test_missing_filename(self):
        """파일명 누락 테스트"""
        data = {
            'content_type': 'image/jpeg'
        }
        serializer = ProfileImageUploadSerializer(data=data)
        assert not serializer.is_valid()
        assert 'filename' in serializer.errors

class TestSocialLoginSerializer:
    
    def test_valid_google_login(self):
        """유효한 구글 로그인 데이터 테스트"""
        data = {
            'code': 'auth_code_123',
            'provider': 'google',
            'redirect_uri': 'http://localhost:3000/callback'
        }
        serializer = SocialLoginSerializer(data=data)
        assert serializer.is_valid()
    
    def test_invalid_provider(self):
        """잘못된 provider 테스트"""
        data = {
            'code': 'auth_code_123',
            'provider': 'facebook'
        }
        serializer = SocialLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'provider' in serializer.errors
    
    def test_missing_code(self):
        """인증 코드 누락 테스트"""
        data = {
            'provider': 'google'
        }
        serializer = SocialLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert 'code' in serializer.errors