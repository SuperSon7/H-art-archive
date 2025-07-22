import pytest
from django.test import TestCase
from django.core import mail
from rest_framework.test import APIClient
from unittest.mock import patch



class TestAccountsAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_user_registration(self):
        """회원가입 테스트"""
        data = {
            "email": "test@example.com",
            "password": "password123",
            "password_confirm": "password123",
            "user_type": "artist",
            "agree_terms": True,
            "agree_privacy": True,
            "language": "ko"
        }
        response = self.client.post('/accounts/register/', data)
        assert response.status_code == 201
        assert response.data['verification_required'] == True
        assert len(mail.outbox) == 1  # 이메일 발송 확인
    
    def test_email_verification(self):
        """이메일 인증 테스트"""
        # 1. 회원가입 먼저
        # 2. 발송된 인증코드로 인증
        data = {"email": "test@example.com", "verification_code": "123456"}
        response = self.client.post('/accounts/verify-email/', data)
        assert response.status_code == 200