# authentication/service/interface_adapters/presenters/login_presenter.py

"""This module defines the LoginPresenter class for handling login response presentation."""

from rest_framework.response import Response


class LoginPresenter:
    """Presenter class responsible for formatting login response data into HTTP responses."""

    def present(self, token_data):
        """Format successful login data into an HTTP response.

        Args:
            token_data: Dictionary containing authentication token data.

        Returns:
            Response: HTTP response with token data and 200 status code.
        """
        return Response(token_data, status=200)

    def present_error(self, error_message):
        """Format login error into an HTTP response.

        Args:
            error_message: String containing error message.

        Returns:
            Response: HTTP response with error message and 401 status code.
        """
        return Response({"error": error_message}, status=401)
