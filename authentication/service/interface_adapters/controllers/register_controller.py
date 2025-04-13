# authentication\service\interface_adapters\controllers\register_controller.py

"""Controller module for handling user registration requests."""

from django.forms import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from service.application.repositories.django_user_repository import DjangoUserRepository
from service.application.use_cases.register_user import RegisterUser
from service.interface_adapters.presenters.register_presenter import RegisterPresenter


class RegisterController(APIView):
    """Controller class for handling user registration API endpoints."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST requests for user registration.

        Args:
            request: The HTTP request object containing user registration data.

        Returns:
            Response: HTTP response with registration result or error message.
        """
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response(
                {"error": "Username, email, and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_repository = DjangoUserRepository()
        use_case = RegisterUser(user_repository)

        try:
            new_user = use_case.execute(
                username=username, email=email, password=password
            )
        except (ValueError, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
        }

        presenter = RegisterPresenter()
        return presenter.present(user_data)
