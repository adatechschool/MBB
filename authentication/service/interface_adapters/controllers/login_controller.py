# authentication/service/interface_adapters/controllers/login_controller.py

"""Controller module for handling user authentication and login functionality."""

from datetime import datetime
import pytz
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from service.application.repositories.django_session_repository import (
    DjangoSessionRepository,
)
from service.application.use_cases.create_session import CreateSession
from service.interface_adapters.presenters.login_presenter import LoginPresenter


class LoginController(APIView):
    """API view controller for handling user login authentication requests."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST requests for user login authentication.

        Args:
            request: HTTP request object containing user credentials

        Returns:
            Response: HTTP response with authentication tokens or error message
        """
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        expires_at = datetime.fromtimestamp(refresh["exp"], tz=pytz.UTC)

        session_repository = DjangoSessionRepository()
        create_session = CreateSession(session_repository)
        create_session.execute(user.user_id, refresh_token, expires_at)

        token_data = {"access": access_token, "refresh": refresh_token}
        presenter = LoginPresenter()
        return presenter.present(
            token_data, expires_at
        )  # pylint: disable=too-many-function-args
