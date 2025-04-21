# authentication\service\interface_adapters\controllers.py

"""Controller for authentication-related HTTP requests and responses."""

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authentication.service.application.use_cases import AuthUseCase
from authentication.service.infrastructure.django_auth_repository import (
    DjangoAuthRepository,
)
from authentication.service.exceptions import (
    UserAlreadyExists,
    AuthenticationFailed,
    TokenBlacklistError,
)
from accounts.service.client import AccountClient
from sessions.service.client import SessionClient
from common.events import publish_event


@method_decorator(csrf_exempt, name="dispatch")
class RegisterController(APIView):
    """Controller handling user registration requests."""

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
            user_id = self.use_case.register(
                data.get("username"), data.get("email"), data.get("password")
            )
        except UserAlreadyExists as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"code": status.HTTP_409_CONFLICT, "message": str(exc)},
                },
                status=status.HTTP_409_CONFLICT,
            )
        AccountClient().create_account(user_id, data.get("username"), data.get("email"))
        return Response(
            {
                "status": "success",
                "data": {"detail": "Registration successful."},
                "error": None,
            },
            status=status.HTTP_201_CREATED,
        )


@method_decorator(csrf_exempt, name="dispatch")
class LoginController(APIView):
    """Controller handling user login requests."""

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
        try:
            tokens = self.use_case.login(data.get("username"), data.get("password"))
        except AuthenticationFailed as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "message": str(exc),
                    },
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        response = Response(
            {
                "status": "success",
                "data": {"access": tokens.access, "refresh": tokens.refresh},
                "error": None,
            }
        )
        secure = not settings.DEBUG
        response.set_cookie(
            key="access_token",
            value=tokens.access,
            httponly=True,
            secure=secure,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh,
            httponly=True,
            secure=secure,
            samesite="Lax",
        )
        SessionClient().create_session(tokens.refresh)
        return response


@method_decorator(csrf_exempt, name="dispatch")
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
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "message": "Refresh token not provided.",
                    },
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            self.use_case.logout(refresh_token)
        except TokenBlacklistError as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"code": status.HTTP_400_BAD_REQUEST, "message": str(exc)},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        publish_event("user.logged_out", {"user_id": request.user.user_id})
        resp = Response(
            {"status": "success", "data": {}, "error": None},
            status=status.HTTP_204_NO_CONTENT,
        )
        resp.delete_cookie("access_token")
        resp.delete_cookie("refresh_token")
        return resp
