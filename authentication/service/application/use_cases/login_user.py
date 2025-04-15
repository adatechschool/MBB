# authentication/service/application/use_cases/login_user.py

"""Module containing the LoginUser use case for user authentication and token generation."""

from multiprocessing import AuthenticationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginUser:
    """Use case for authenticating users and generating JWT tokens.

    This class handles user login by validating credentials and generating
    JSON Web Tokens (JWT) for authenticated users.
    """

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str):
        """Authenticate user and generate JWT tokens.

        Args:
            email (str): User's email address
            password (str): User's password

        Returns:
            dict: Dictionary containing access and refresh tokens

        Raises:
            Exception: If credentials are invalid
        """
        user = authenticate(username=email, password=password)
        if not user:
            raise AuthenticationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}
