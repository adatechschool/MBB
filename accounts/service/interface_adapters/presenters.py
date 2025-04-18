# accounts\service\interface_adapters\presenters.py

"""Presenter class for handling account-related API responses."""

from rest_framework.response import Response


class AccountPresenter:
    """Transforms account domain models into API responses."""

    def present(self, account):
        """Transform account domain model into API response.

        Args:
            account: Account domain model to be transformed

        Returns:
            Response: DRF Response object containing account data with 200 status
        """
        return Response(account.to_dict(), status=200)
