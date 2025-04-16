# authentication/service/application/repositories/django_user_repository.py

"""Django implementation of the user repository interface for authentication operations."""

from typing import Optional
from service.application.repositories.user_repository import UserRepositoryInterface
from service.core.entities.user import UserEntity
from users.models import User


class DjangoUserRepository(UserRepositoryInterface):
    """Django implementation of user repository for authentication operations."""

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(email=email)
            return UserEntity(
                user_id=user.pk,
                username=user.username,
                email=user.email,
                hashed_password=user.password,
            )
        except User.DoesNotExist:
            return None

    def create_user(self, username: str, email: str, password: str) -> UserEntity:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return UserEntity(
            user_id=user.pk,
            username=user.username,
            email=user.email,
            hashed_password=user.password,
        )
