# authentication/service/application/use_cases/login_user.py

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginUser:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, email: str, password: str):
        # Authenticate the user using Django's authentication backend
        user = authenticate(email=email, password=password)
        if not user:
            raise Exception("Invalid credentials")

        # Generate a pair of tokens (access and refresh)
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
