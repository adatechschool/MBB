# authentication/service/interface_adapters/gateways/django_user_repository.py

"""Django implementation of the user repository interface for authentication operations."""

from service.application.repositories.user_repository import UserRepositoryInterface
from service.core.entities.user import UserEntity
from service.models import User


class DjangoUserRepository(UserRepositoryInterface):
    """Django implementation of user repository for authentication operations."""

    def get_by_email(self, email: str) -> UserEntity:
        try:
            user = User.objects.get(email=email)
            return UserEntity(
                user_id=user.pk,
                username=user.username,
                email=user.email,
                hashed_password=user.password,
            )
        except User.objects.model.DoesNotExist as exc:
            raise ValueError("User not found") from exc

    def create_user(self, username: str, email: str, password: str) -> UserEntity:
        user = User.objects.create(username=username, email=email, password=password)
        return UserEntity(
            user_id=user.pk,
            username=user.username,
            email=user.email,
            hashed_password=user.password,
        )
