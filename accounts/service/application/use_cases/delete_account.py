# accounts\service\application\use_cases\delete_account.py

"""This module contains the DeleteAccount use case which handles account deletion functionality."""

from service.application.repositories.account_repository import (
    AccountRepositoryInterface,
)


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
