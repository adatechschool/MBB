# authentication/service/application/use_cases/register_user.py

from service.application.repositories.user_repository import UserRepositoryInterface
from service.core.entities.user import UserEntity


class RegisterUser:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, username: str, email: str, password: str) -> UserEntity:
        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise ValueError("A user with this email already exists")

        new_user = self.user_repository.create_user(
            username=username, email=email, password=password
        )
        return new_user
