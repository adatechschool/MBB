# authentication\service\authentication.py

"""Authentication service module for JWT token handling via cookies."""

from rest_framework_simplejwt.authentication import JWTAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    """
    A SimpleJWT authentication backend that will first look
    for Authorization: Bearer <token>, then fall back to the
    'access_token' cookie.
    """

    def get_header(self, request):
        header = super().get_header(request)
        if header is not None:
            return header

        token = request.COOKIES.get("access_token")
        if token:
            return f"Bearer {token}".encode("utf-8")
        return None

    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            raw_token = request.COOKIES.get("access_token", None)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        reason = CsrfViewMiddleware().process_view(request._request, None, (), {})
        if reason:
            raise AuthenticationFailed(f"CSRF Failed: {reason}")
        return self.get_user(validated_token), validated_token
