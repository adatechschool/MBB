# authentication\service\interface_adapters\presenters\register_presenter.py

"""Presenter module for handling user registration requests."""

from rest_framework.response import Response


class RegisterPresenter:
    """Presenter class for handling user registration requests."""

    def present(self, user_data: dict) -> Response:
        """Present the registration response.

        Args:
            user_data (dict): The registered user's data.

        Returns:
            Response: DRF Response object containing success message and user data.
        """
        return Response(
            {
                "message": "Registration successful",
                "user": user_data,
            }
        )
