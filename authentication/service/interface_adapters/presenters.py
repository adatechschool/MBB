# authentication\service\interface_adapters\presenters.py

"""Presenter for formatting authentication HTTP responses."""

from common.presenters import BasePresenter


class AuthPresenter(BasePresenter):
    """Presenter class responsible for formatting authentication-related HTTP responses."""

    def present_register(self):
        """Format successful registration response.

        Returns:
            dict: Response containing success message with 201 status code.
        """
        return self.success({"detail": "Registration successful."}, http_status=201)

    def present_login(self, tokens):
        """Format successful login response.

        Args:
            tokens: Object containing access and refresh tokens.

        Returns:
            dict: Response containing access and refresh tokens.
        """
        return self.success({"access": tokens.access, "refresh": tokens.refresh})

    def present_logout(self):
        """Format successful logout response.

        Returns:
            dict: Response containing empty body with 204 status code.
        """
        return self.success({}, http_status=204)

    def present_error(self, message: str, code: int = 400):
        """Format error response with provided message and code."""
        return self.error(message, code)
