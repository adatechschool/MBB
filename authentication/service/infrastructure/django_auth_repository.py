# authentication/service/infrastructure/django_auth_repository.py

"""Django ORM implementation of the authentication repository interface."""

from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from authentication.service.exceptions import (
    UserAlreadyExists,
    AuthenticationFailed,
    TokenBlacklistError,
)
from authentication.service.application.repositories import AuthRepositoryInterface
from authentication.service.domain.entities import AuthModel
from common.models import User, Role


class DjangoAuthRepository(AuthRepositoryInterface):
    """Django ORM implementation of authentication repository for managing user authentication
    operations.
    """

    def register(self, username: str, email: str, password: str) -> str:
        default_role, _ = Role.objects.get_or_create(role_name="user", defaults={})
        user = User(username=username, email=email, role=default_role)
        user.set_password(password)
        try:
            user.save()
        except IntegrityError as exc:
            raise UserAlreadyExists(str(exc)) from exc
        return str(user.user_id)

    def authenticate(self, username: str, password: str) -> AuthModel:
        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid credentials")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return AuthModel(access=access_token, refresh=refresh_token)

    def blacklist(self, refresh_token: str) -> None:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as exc:
            raise TokenBlacklistError(
                "Invalid or expired refresh token or already blacklisted."
            ) from exc
