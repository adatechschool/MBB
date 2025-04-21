# accounts\service\interface_adapters\presenters.py

"""Presenter for formatting account HTTP responses."""

from common.presenters import BasePresenter
from common.dtos import AccountDTO


class AccountPresenter(BasePresenter):
    """Presenter class responsible for formatting account-related HTTP responses."""

    def present_account(self, entity: AccountDTO):
        """Format an account entity into a successful HTTP response.

        Args:
            entity: The account entity to format

        Returns:
            A formatted HTTP response containing the account data
        """
        return self.success(entity.to_dict(), http_status=200)

    def present_not_found(self):
        """Format a not found error response.

        Returns:
            A formatted HTTP 404 error response
        """
        return self.error("Account not found.", code=404)

    def present_deleted(self):
        """Format a successful deletion response.

        Returns:
            A formatted HTTP 204 response indicating successful deletion
        """
        return self.success({}, http_status=204)

    def present_error(self, message: str, code: int = 400):
        """Format error response with provided message and code."""
        return self.error(message, code)
