# authentication\service\authentication.py

"""Authentication service module for JWT token handling via cookies."""

from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(BaseAuthentication):
    """
    Example stub: pull JWT from a cookie instead of Authorization header.
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if not raw_token:
            return None
        validated = JWTAuthentication().get_validated_token(raw_token)
        user = JWTAuthentication().get_user(validated)
        return (user, validated)
