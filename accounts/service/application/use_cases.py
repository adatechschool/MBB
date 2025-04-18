# accounts\service\application\use_cases.py

"""Module containing the UseCase class for managing account updates."""

from typing import Optional
from accounts.service.application.repositories import AccountRepositoryInterface


class GetAccount:
    """Use case that retrieves an account by its user ID from the account repository."""

    def __init__(self, account_repository: AccountRepositoryInterface):
        self.account_repository = account_repository

    def execute(self, user_id: int):
        """Retrieve an account by user ID.

        Args:
            user_id (int): The ID of the user whose account to retrieve

        Returns:
            Account: The retrieved account

        Raises:
            ValueError: If no account is found for the given user ID
        """
        account = self.account_repository.get_account(user_id)
        if account is None:
            raise ValueError("Account not found")
        return account


class UpdateAccount:
    """Use case for updating an existing account with new information.

    This class handles the business logic for updating account details including
    username, email, bio, and profile picture.
    """

    def __init__(self, account_repository: AccountRepositoryInterface):
        self.account_repository = account_repository

    def execute(
        self,
        user_id: int,
        username: str,
        email: str,
        bio: str,
        profile_picture: Optional[str],
    ):
        """Update an existing account with new information.

        Args:
            user_id: Unique identifier of the account to update
            username: New username for the account
            email: New email address for the account
            bio: New biography text for the account
            profile_picture: New profile picture bytes data

        Returns:
            Updated account object
        """
        account = self.account_repository.update_account(
            user_id, username, email, bio, profile_picture
        )
        return account


class DeleteAccount:
    """Use case for deleting a user account from the system."""

    def __init__(self, account_repository: AccountRepositoryInterface):
        self.account_repository = account_repository

    def execute(self, user_id: int):
        """Delete a user account from the system.

        Args:
            user_id (int): The ID of the user account to delete.

        Raises:
            ValueError: If the account with the given user_id is not found.
        """
        account = self.account_repository.get_account(user_id)
        if account is None:
            raise ValueError("Account not found")
        self.account_repository.delete_account(user_id)
