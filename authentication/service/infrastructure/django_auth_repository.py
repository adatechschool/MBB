# authentication/service/infrastructure/django_auth_repository.py

"""Django ORM implementation of the authentication repository interface."""

from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.service.application.repositories import AuthRepositoryInterface
from authentication.service.core.entities import AuthTokens

User = get_user_model()


class DjangoAuthRepository(AuthRepositoryInterface):
    """Django ORM implementation of authentication repository for managing user authentication
    operations.
    """

    def register(self, username: str, email: str, password: str) -> None:
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

    def authenticate(self, username: str, password: str) -> AuthTokens:
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValueError("Invalid credentials")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return AuthTokens(access=access_token, refresh=refresh_token)

    def blacklist(self, refresh_token: str) -> None:
        token = RefreshToken(refresh_token)
        token.blacklist()
