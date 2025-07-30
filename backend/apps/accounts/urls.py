from django.urls import path
from .views import (
    SignUpView,
    SendVerificationEmailView,
    VerifyEmailView,
    LoginView,
    TokenRefreshView,
    LogoutView,
)


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('send-verification/', SendVerificationEmailView.as_view(), name='send_verification'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
