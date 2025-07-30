from django.contrib.auth.backends import ModelBackend
from .models import User
from typing import Optional
from django.http import HttpRequest

def authenticate(
    self,
    request: Optional[HttpRequest],
    email: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs
) -> Optional[User]:
    """
    이메일과 비밀번호로 사용자 인증을 수행하는 메서드(로그인)

    Args:
        request (Optional[HttpRequest]): 요청 객체. 일부 인증 백엔드에서는 사용되지 않을 수 있음.
        email (Optional[str], optional): 사용자의 이메일. Defaults to None.
        password (Optional[str], optional): 사용자의 비밀번호. Defaults to None.

    Returns:
        Optional[User]: 인증에 성공하면 User 객체를, 실패하면 None을 반환.
    """
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
