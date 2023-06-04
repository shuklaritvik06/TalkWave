from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
