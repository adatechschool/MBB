# accounts\service\interface_adapters\controllers\account_controller.py

"""Controller for handling account-related HTTP requests and responses."""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from service.application.repositories.django_account_repository import (
    DjangoAccountRepository,
)
from service.application.use_cases.get_account import GetAccount
from service.application.use_cases.update_account import UpdateAccount
from service.application.use_cases.delete_account import DeleteAccount
from service.interface_adapters.presenters.account_presenter import AccountPresenter

USER_ID_REQUIRED = "User ID is required."


class AccountController(APIView):
    """Controller class that handles HTTP requests and responses for account-related operations."""

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        """Handle GET request to retrieve an account by user ID.

        Args:
            request: The HTTP request object
            user_id: The ID of the user whose account to retrieve

        Returns:
            Response object containing the account data or error message
        """
        if user_id is None:
            user_id = request.user.user_id

        repository = DjangoAccountRepository()
        use_case = GetAccount(repository)
        try:
            account = use_case.execute(user_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        presenter = AccountPresenter()
        return presenter.present(account)

    def put(self, request, user_id=None):
        """Handle PUT request to update an existing account.

        Args:
            request: The HTTP request object containing account update data
            user_id: The ID of the user whose account to update

        Returns:
            Response object containing the updated account data or error message
        """
        if user_id is None:
            user_id = request.user.user_id
        username = request.data.get("username")
        email = request.data.get("email")
        bio = request.data.get("bio", "")
        profile_picture = request.data.get("profile_picture")
        if not username or not email:
            return Response(
                {"error": "Username and email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        repository = DjangoAccountRepository()
        use_case = UpdateAccount(repository)
        account = use_case.execute(user_id, username, email, bio, profile_picture)
        presenter = AccountPresenter()
        return presenter.present(account)

    def delete(self, request, user_id=None):
        """Delete a user account.

        Args:
            request: HTTP request object
            user_id: Optional user_id, if none provided, use authenticated user's ID.

        Returns:
            Response: HTTP response indicating deletion status
        """
        user_id = user_id or request.user.user_id

        repository = DjangoAccountRepository()
        use_case = DeleteAccount(repository)

        try:
            use_case.execute(user_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        response = Response(
            {"message": "Account deleted successfully."}, status=status.HTTP_200_OK
        )

        response.delete_cookie("accessToken", path="/")
        response.delete_cookie("refreshToken", path="/")

        return response
