import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="HDS2020@anything.com", 
        password="password1234", 
        username = "HOTBOy", 
        is_active=True
)

@pytest.mark.django_db
class TestLoginOut:
    def test_user_login(self, client: APIClient, test_user: User) -> None:
        """로그인 테스트"""
        
        data = {
            "email": "HDS2020@anything.com", 
            "password": "password1234", 
            "username": "HOTBOy"
        }
        
        response = client.post(reverse("login"), data)
        print(response.data)
        assert response.status_code == 200
        assert 'access_token' in response.data
    
    def test_user_logout(self, client: APIClient, test_user: User) -> None:
        """로그아웃 테스트"""
        client.force_authenticate(user=test_user)
        response = client.post(reverse("logout"))
        
        assert response.status_code == 204
        assert response.content == b''