# authentication/service/interface_adapters/controllers/login_controller.py

"""Controller module handling user login authentication requests."""

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from service.application.repositories.django_user_repository import DjangoUserRepository
from service.application.use_cases.login_user import LoginUser
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

        user_repository = DjangoUserRepository()
        use_case = LoginUser(user_repository)

        try:
            # In this JWT approach, the use case returns a dict with refresh and access tokens.
            token_data = use_case.execute(email, password)
        except Exception as e:
            raise AuthenticationFailed(str(e)) from e

        presenter = LoginPresenter()
        return presenter.present(token_data)
