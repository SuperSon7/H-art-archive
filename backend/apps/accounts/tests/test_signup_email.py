import pytest
from django.test import TestCase
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class SignupEmailTestCase:
    
    def test_user_registration(self, client):
        """회원가입 테스트"""
        
        data = {
            "email": "test@example.com",
            "username": "한동숙",
            "password": "password123",
            "password_confirm": "password123",
            "user_type": "artist",
            "agree_terms": True,
            "agree_privacy": True,
            "language": "ko"
        }
        response = client.post(reverse("signup"), data)
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