# accounts/service/interface_adapters/presenters.py

"""Presenter for formatting account HTTP responses."""

from rest_framework.response import Response
from rest_framework import status

from accounts.service.core.entities import AccountEntity


class Presenter:
    """Presenter for formatting account HTTP responses."""

    def present_account(self, entity: AccountEntity) -> Response:
        """Format an account entity into an HTTP response.

        Args:
            entity: The account entity to format

        Returns:
            Response object with account data and 200 status code
        """
        data = entity.to_dict()
        return Response(data, status=status.HTTP_200_OK)

    def present_not_found(self) -> Response:
        """Format a not found HTTP response.

        Returns:
            Response object with 404 status code and error message
        """
        return Response(
            {"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND
        )

    def present_deleted(self) -> Response:
        """Format a deleted HTTP response.

        Returns:
            Response object with 204 status code
        """
        return Response(status=status.HTTP_204_NO_CONTENT)
