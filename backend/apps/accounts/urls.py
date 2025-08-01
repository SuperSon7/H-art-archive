from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    LogoutView,
    SendVerificationEmailView,
    SignUpView,
    SocialLoginView,
    TokenRefreshView,
    UserInfoViewSet,
    VerifyEmailView,
)

router = DefaultRouter()
router.register(r'users', UserInfoViewSet, basename='user')

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('send-verification/', SendVerificationEmailView.as_view(), name='send_verification'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('social-login/', SocialLoginView.as_view(), name='social-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls