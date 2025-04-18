# accounts/service/application/use_cases.py

"""Use case layer for account operations."""

from typing import Optional

from accounts.service.application.repositories import AccountRepositoryInterface
from accounts.service.core.entities import AccountEntity


class AccountUseCase:
    """Use case layer for account operations."""

    def __init__(self, repo: AccountRepositoryInterface):
        self.repo = repo

    def get_account(self, user_id: int) -> Optional[AccountEntity]:
        """Retrieve an account by user ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The account entity if found, None otherwise.
        """
        return self.repo.get_account(user_id)

    def update_account(
        self,
        user_id: int,
        username: str,
        email: str,
        bio: str,
        profile_picture: Optional[str],
    ) -> AccountEntity:
        """Update an account with new information.

        Args:
            user_id: The unique identifier of the user
            username: The new username
            email: The new email address
            bio: The new biography text
            profile_picture: Optional URL to profile picture

        Returns:
            The updated account entity
        """
        return self.repo.update_account(user_id, username, email, bio, profile_picture)

    def delete_account(self, user_id: int) -> None:
        """Delete an account.

        Args:
            user_id: The unique identifier of the user to delete
        """
        self.repo.delete_account(user_id)
