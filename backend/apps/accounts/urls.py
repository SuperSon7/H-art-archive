from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignUpView,
    SendVerificationEmailView,
    VerifyEmailView,
    LoginView,
    TokenRefreshView,
    LogoutView,
    UserInfoViewSet,
    SocialLoginView,
)

router = DefaultRouter()
router.register(r'users', UserInfoViewSet, basename='user')

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('send-verification/', SendVerificationEmailView.as_view(), name='send_verification'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('social-login/', SocialLoginView.as_veiw(), name='social-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls