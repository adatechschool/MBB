# accounts\service\application\repositories\account_repository.py

"""Repository interface for account management operations."""

from abc import ABC, abstractmethod
from typing import Optional
from accounts.service.core.entities.account import AccountEntity


class AccountRepositoryInterface(ABC):
    """Interface defining the contract for account management operations in the repository layer."""

    @abstractmethod
    def get_account(self, user_id: int) -> Optional[AccountEntity]:
        """Retrieve an account by user ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The account entity if found, None otherwise.
        """

    @abstractmethod
    def update_account(
        self,
        user_id: int,
        username: str,
        email: str,
        bio: str,
        profile_picture: Optional[str],
    ) -> AccountEntity:
        """Update an account with the given information.

        Args:
            user_id: The unique identifier of the user.
            username: The new username for the account.
            email: The new email address for the account.
            bio: The new biography text for the account.
            profile_picture: Optional bytes data for the profile picture.

        Returns:
            The updated account entity.
        """

    @abstractmethod
    def delete_account(self, user_id: int) -> None:
        """Delete an account with the given user ID.

        Args:
            user_id: The unique identifier of the user to delete.
        """
