from .utils.social_auth import *
from apps.accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def login_with_social(provider, code, redirect_uri):
    adapter = SocialAdapterRegistry.get_adapter(provider)
    access_token = adapter.exchange_code_for_token(code, redirect_uri)
    user_info = adapter.get_user_info(access_token)
    user_data = adapter.normalize_user_data(user_info)

    user, _ = User.objects.get_or_create(
        social_type=user_data["provider"],
        social_id=user_data["social_id"],
        defaults={"email": user_data["email"]}
    )

    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user_type": user.user_type,
    }