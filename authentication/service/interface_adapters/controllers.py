# authentication\service\interface_adapters\controllers.py

"""Controller for authentication-related HTTP requests and responses."""

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from authentication.service.application.use_cases import AuthUseCase
from authentication.service.infrastructure.django_auth_repository import (
    DjangoAuthRepository,
)
from authentication.service.exceptions import (
    UserAlreadyExists,
    AuthenticationFailed,
    TokenBlacklistError,
)
from sessions.service.client import SessionClient
from common.events import publish_event
from common.response import success, error

COOKIE_PATH = "/"
ACCESS_COOKIE_AGE = (
    getattr(settings, "SIMPLE_JWT", {}).get("ACCESS_TOKEN_LIFETIME").total_seconds()
)
REFRESH_COOKIE_AGE = (
    getattr(settings, "SIMPLE_JWT", {}).get("REFRESH_TOKEN_LIFETIME").total_seconds()
)


class CsrfRefreshController(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return success(
            data={},
            http_status=status.HTTP_200_OK
        )

class RegisterController(APIView):
    """Controller handling user registration requests."""

    authentication_classes = []
    permission_classes = [AllowAny]
    use_case = AuthUseCase(DjangoAuthRepository())

    def post(self, request):
        """Handle POST requests for user registration.

        Args:
            request: HTTP request object containing registration data

        Returns:
            HTTP response with registration result
        """
        data = request.data
        try:
            user_id = self.use_case.register(  # noqa
                data.get("username"), data.get("email"), data.get("password")
            )
        except UserAlreadyExists as exc:
            return error(
                message=str(exc),
                http_status=status.HTTP_409_CONFLICT,
            )
        publish_event(
            "user.registered",
            {
                "user_id": user_id,
                "username": data.get("username"),
                "email": data.get("email"),
            }
        )
        return success(
            {"detail": "Registration successful."},
            http_status=status.HTTP_201_CREATED,
        )


class LoginController(APIView):
    """Controller handling user login requests."""

    authentication_classes = []
    permission_classes = [AllowAny]
    use_case = AuthUseCase(DjangoAuthRepository())

    def post(self, request):
        """Handle POST requests for user login.

        Args:
            request: HTTP request object containing login credentials

        Returns:
            HTTP response with login result and authentication cookies
        """
        data = request.data
        email = data.get("email")
        password = data.get("password")
        try:
            tokens = self.use_case.login(email, password)
        except AuthenticationFailed as exc:
            return error(
                message=str(exc),
                http_status=status.HTTP_401_UNAUTHORIZED,
            )
        response = success(
            {"access": tokens.access, "refresh": tokens.refresh},
            http_status=status.HTTP_200_OK,
        )
        secure_flag = settings.COOKIE_SECURE
        response.set_cookie(
            key="access_token",
            value=tokens.access,
            max_age=int(ACCESS_COOKIE_AGE),
            httponly=True,
            secure=secure_flag,
            samesite="Lax",
            path=COOKIE_PATH,
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh,
            max_age=int(REFRESH_COOKIE_AGE),
            httponly=True,
            secure=secure_flag,
            samesite="Lax",
            path=COOKIE_PATH,
        )
        SessionClient().create_session(
            refresh_token=tokens.refresh,
            access_token=tokens.access,
        )
        publish_event("user.logged_in", {"email": email})
        return response


class LogoutController(APIView):
    """Controller handling user logout requests by invalidating
    and removing authentication tokens."""

    permission_classes = [IsAuthenticated]
    use_case = AuthUseCase(DjangoAuthRepository())

    def post(self, request):
        """Handle POST request for user logout by
        invalidating the refresh token and removing auth cookies.

        Args:
            request: HTTP request object containing auth cookies

        Returns:
            Response: HTTP response indicating logout success or error
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return error(
                message="Refresh token not provided.",
                http_status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            self.use_case.logout(refresh_token)
        except TokenBlacklistError as exc:
            return error(
                message=str(exc),
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        publish_event("user.logged_out", {"user_id": request.user.user_id})
        resp = success(http_status=status.HTTP_204_NO_CONTENT)
        resp.delete_cookie("access_token", path=COOKIE_PATH)
        resp.delete_cookie("refresh_token", path=COOKIE_PATH)
        return resp
