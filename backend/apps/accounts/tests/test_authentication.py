import jwt
import pytest
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from apps.accounts.authentication import JWTAuthentication


@pytest.mark.django_db
class TestJWTAuthentication:
    
    def setup_method(self):
        self.auth = JWTAuthentication()
        self.factory = APIRequestFactory()
    
    def test_no_auth_header(self):
        """Authorization 헤더가 없는 경우 테스트"""
        request = self.factory.get('/')
        result = self.auth.authenticate(request)
        assert result is None
    
    def test_invalid_auth_header_format(self):
        """잘못된 Authorization 헤더 형식 테스트"""
        request = self.factory.get('/', HTTP_AUTHORIZATION='InvalidToken')
        result = self.auth.authenticate(request)
        assert result is None
    
    def test_valid_token(self, user):
        """유효한 토큰으로 인증 테스트"""
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        result = self.auth.authenticate(request)
        assert result is not None
        assert result[0] == user
    
    def test_expired_token(self, user):
        """만료된 토큰 테스트"""
        # 만료된 토큰 생성
        payload = {
            'user_id': user.id,
            'exp': 1000  # 과거 시간
        }
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        with pytest.raises(AuthenticationFailed, match='Token expired'):
            self.auth.authenticate(request)
    
    def test_invalid_token(self):
        """잘못된 토큰 테스트"""
        request = self.factory.get('/', HTTP_AUTHORIZATION='Bearer invalid_token')
        with pytest.raises(AuthenticationFailed, match='Invalid token'):
            self.auth.authenticate(request)

    def test_nonexistent_user(self):
        """존재하지 않는 사용자 토큰 테스트"""
        payload = {
            'user_id': 99999,
            'exp': 9999999999  # 미래 시간
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        with pytest.raises(AuthenticationFailed, match='User not found'):
            self.auth.authenticate(request)