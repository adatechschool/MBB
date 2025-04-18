# accounts\service\application\use_cases\get_account.py

"""Use case for retrieving an account by user ID."""

from accounts.service.application.repositories.account_repository import (
    AccountRepositoryInterface,
)


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
