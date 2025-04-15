# authentication/service/interface_adapters/controllers/login_controller.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from service.interface_adapters.presenters.login_presenter import LoginPresenter

# NEW IMPORTS for session creation:
from datetime import datetime
import pytz  # make sure to add pytz to your dependencies if not already present
from service.application.use_cases.create_session import CreateSession
from service.application.repositories.django_session_repository import (
    DjangoSessionRepository,
)


class LoginController(APIView):
    """API view controller for handling user login authentication requests."""

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate the user.
        user = authenticate(username=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")

        # Generate JWT tokens via SimpleJWT.
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Calculate the expiration time from the refresh token payload.
        # The token's "exp" claim is a UNIX epoch timestamp.
        expires_at = datetime.fromtimestamp(refresh["exp"], tz=pytz.UTC)

        # Create a session record for the refresh token.
        session_repository = DjangoSessionRepository()
        create_session = CreateSession(session_repository)
        # 'user.user_id' should be the unique user identifier
        session_entity = create_session.execute(  # noqa
            user.user_id, refresh_token, expires_at
        )
        # (You may log or inspect session_entity if needed)

        # Return tokens using the login presenter.
        token_data = {"access": access_token, "refresh": refresh_token}
        presenter = LoginPresenter()
        return presenter.present(token_data)
