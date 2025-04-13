# authentication/service/interface_adapters/presenters/logout_presenter.py

"""Presenter module for handling logout response presentation in the authentication service."""

from rest_framework.response import Response


class LogoutPresenter:
    """Presenter class responsible for formatting and returning logout responses."""

    def present(self, success: bool) -> Response:
        """Present the logout response based on success status.

        Args:
            success (bool): Indicates if logout was successful

        Returns:
            Response: HTTP response with appropriate message and status code
        """
        if success:
            return Response({"message": "Successfully logged out"})
        return Response({"error": "Failed to log out"}, status=400)

    def format_error_message(self, error_msg: str) -> dict:
        """Format error message into standard response structure.

        Args:
            error_msg (str): Error message to format

        Returns:
            dict: Formatted error message dictionary
        """
        return {"error": error_msg}
