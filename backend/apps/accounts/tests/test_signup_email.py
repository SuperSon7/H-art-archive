import re
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.task import send_verification_email_task

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.unit
@pytest.mark.django_db
class TestSignupEmail:
    def test_user_registration(self, client):
        """회원가입 테스트"""

        data = {
            "email": "test@example.com",
            "username": "한동숙",
            "password": "password123",
            "password_confirm": "password123",
            "user_type": "artist",
        }

        response = client.post(reverse("signup"), data)

        assert response.status_code == 201
        assert response.data["verification_required"]

    @patch(
        "apps.accounts.views.send_verification_email_task.delay",
        lambda email, token: send_verification_email_task(email, token),
    )
    @patch("apps.accounts.views.check_email_throttle", lambda x: None)
    @pytest.mark.integration
    def test_email_verification(self, client):
        """이메일 인증 테스트"""
        # 1. 회원가입 먼저
        data = {
            "email": "TETEMU@example.com",
            "username": "템무",
            "password": "password123",
            "password_confirm": "password123",
            "user_type": "artist",
        }

        response = client.post(reverse("signup"), data)
        assert response.status_code == 201
        user_id = response.data["user_id"]
        email = data["email"]

        # 2. 발송된 인증코드로 인증
        send_response = client.post(
            reverse("send_verification"), data={"uid": user_id, "email": email}
        )
        assert send_response.status_code == 200
        assert send_response.data["success"]
        assert "인증 이메일을 발송하였습니다" in send_response.data["message"]
        assert len(mail.outbox) == 1

        # 3. 이메일 본문에서 토큰 추출
        email_body = mail.outbox[0].body
        token = extract_token_from_email_body(email_body)
        # 4. 토큰으로 이메일 인증
        verify_response = client.post(
            reverse("verify_email"),  # 너의 URLconf에서 이 이름으로 등록돼야 함
            data={"token": token},
            content_type="application/json",
        )
        assert verify_response.status_code == 200
        assert verify_response.data["success"] is True
        assert "이메일 인증이 완료" in verify_response.data["message"]

        user = User.objects.get(email=email)

        # 5. 유저 상태 확인
        user.refresh_from_db()
        assert user.is_active is True


@pytest.mark.unit
def extract_token_from_email_body(email_body: str) -> str:
    # 예: http://localhost:8000/api/v1/accounts/verify-email/?token=xxxxx
    match = re.search(r"token=([a-zA-Z0-9\.\-_]+)", email_body)
    if not match:
        raise ValueError("이메일 본문에서 토큰을 찾을 수 없습니다.")
    return match.group(1)
