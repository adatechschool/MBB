# authentication/service/interface_adapters/controllers/login_controller.py

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from service.interface_adapters.presenters.login_presenter import LoginPresenter


class LoginController(APIView):
    """API view controller for handling user login authentication requests."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST requests for user login.

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

        # Authenticate the user using Django's authenticate function.
        user = authenticate(username=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")

        # Generate JWT tokens using the SimpleJWT refresh mechanism.
        refresh = RefreshToken.for_user(user)
        token_data = {"access": str(refresh.access_token), "refresh": str(refresh)}

        presenter = LoginPresenter()
        return presenter.present(token_data)
