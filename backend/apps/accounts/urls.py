from django.urls import path
from .views import (
    SignUpView,
    SendVerificationEmailView,
    VerifyEmailView,
)


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('send-verification/', SendVerificationEmailView.as_view(), name='send_verification'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
]
