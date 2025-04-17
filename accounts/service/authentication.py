# pylint: skip-file
# accounts/service/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Read the JWT access token from the 'accessToken' or 'refreshToken' cookie,
    falling back to the Authorization header if neither is present.
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get("accessToken") or request.COOKIES.get(
            "refreshToken"
        )
        if raw_token:
            validated_token = self.get_validated_token(raw_token)
            return (self.get_user(validated_token), validated_token)
        return super().authenticate(request)
