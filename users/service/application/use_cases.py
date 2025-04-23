# users\service\application\use_cases.py

from typing import List

from users.service.application.repositories import UserRepositoryInterface
from common.dtos import AccountDTO


class UserUseCase:
    """Use case layer for user operations."""

    def __init__(self, repo: UserRepositoryInterface):
        self.repo = repo

    def get_all_users(self) -> List[AccountDTO]:
        """Retrieve all user accounts."""
        return self.repo.get_all_users()
