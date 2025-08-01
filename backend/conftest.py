import os

import pytest
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def pytest_configure():
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env.test"))
User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testuser123',
        user_type='artist'
    )

@pytest.fixture
def social_user():
    return User.objects.create(
        email='social@example.com',
        social_type='google',
        social_id='123456789',
        user_type='collector'
    )

@pytest.fixture
def active_user(db):
    return User.objects.create_user(
        email='active@example.com',
        username='activeuser',
        password='testuser123',
        user_type='artist',
        is_active=True
    )
    
@pytest.fixture
def authenticated_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client