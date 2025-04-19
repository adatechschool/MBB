# authentication\service\interface_adapters\controllers.py

"""Controller for authentication-related HTTP requests and responses."""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings

from authentication.service.application.use_cases import AuthUseCase
from authentication.service.infrastructure.django_auth_repository import (
    DjangoAuthRepository,
)
from authentication.service.interface_adapters.presenters import AuthPresenter


class RegisterController(APIView):
    """Controller handling user registration requests."""

    permission_classes = [AllowAny]
    use_case = AuthUseCase(DjangoAuthRepository())
    presenter = AuthPresenter()

    def post(self, request):
        """Handle POST requests for user registration.

        Args:
            request: HTTP request object containing registration data

        Returns:
            HTTP response with registration result
        """
        data = request.data
        try:
            self.use_case.register(
                data.get("username"), data.get("email"), data.get("password")
            )
        except ValueError as exc:
            return self.presenter.present_error(str(exc))
        return self.presenter.present_register()


class LoginController(APIView):
    """Controller handling user login requests."""

    permission_classes = [AllowAny]
    use_case = AuthUseCase(DjangoAuthRepository())
    presenter = AuthPresenter()

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
        except ValueError:
            return self.presenter.present_error("Invalid credentials.")
        response = self.presenter.present_login(tokens)
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
        return response


class LogoutController(APIView):
    """Controller handling user logout requests by invalidating
    and removing authentication tokens."""

    permission_classes = [IsAuthenticated]
    use_case = AuthUseCase(DjangoAuthRepository())
    presenter = AuthPresenter()

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
            return self.presenter.present_error(
                "Refresh token not provided.", code=status.HTTP_401_UNAUTHORIZED
            )
        try:
            self.use_case.logout(refresh_token)
        except ValueError as exc:
            return self.presenter.present_error(str(exc))
        response = self.presenter.present_logout()
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
