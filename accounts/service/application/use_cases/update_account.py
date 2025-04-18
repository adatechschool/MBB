# accounts\service\application\use_cases\update_account.py

"""Module containing the UpdateAccount use case for managing account updates."""

from typing import Optional
from accounts.service.application.repositories.account_repository import (
    AccountRepositoryInterface,
)


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
