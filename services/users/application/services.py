from services.users.domain.models import User
from services.users.infrastructure.repositories import UserRepository
from datetime import datetime,timezone

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        user.created_at = datetime.now(timezone.utc)
        return self.user_repository.create(user)

    def get_user(self, user_id: str) -> User:
        return self.user_repository.get(user_id)

    def update_user(self, user: User) -> User:
        user.updated_at = datetime.now(timezone.utc)
        return self.user_repository.update(user)

    def delete_user(self, user_id: str) -> None:
        self.user_repository.delete(user_id)
