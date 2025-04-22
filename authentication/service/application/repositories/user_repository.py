# authentication/service/application/repositories/user_repository.py

"""Repository interface for user-related database operations."""

from typing import Optional
from abc import ABC, abstractmethod
from service.core.entities.user import UserEntity


class UserRepositoryInterface(ABC):
    """Abstract base class defining the interface for user repository operations."""

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Retrieve a user entity based on email.

        Returns:
            Optional[UserEntity]: The user entity if found, or None otherwise.
        """

    @abstractmethod
    def create_user(self, username: str, email: str, password: str) -> UserEntity:
        """Create and return a new user entity."""
