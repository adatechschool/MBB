# authentication/service/interface_adapters/gateways/django_user_repository.py

from service.application.repositories.user_repository import UserRepositoryInterface
from service.core.entities.user import UserEntity
from service.models import User

class DjangoUserRepository(UserRepositoryInterface):
    def get_by_email(self, email: str) -> UserEntity:
        try:
            user = User.objects.get(email=email)
            return UserEntity(
                id=user.pk,
                username=user.username,
                email=user.email,
                hashed_password=user.password
            )
        except User.DoesNotExist:
            return None
