# users\service\application\repositories.py

"""Repository interface for user management operations."""

from abc import ABC, abstractmethod

from typing import List
from common.dtos import AccountDTO


class UserRepositoryInterface(ABC):
    """Interface defining user repository contract."""

    @abstractmethod
    def get_all_users(self) -> List[AccountDTO]:
        """Retrieve all user accounts as DTOs."""
