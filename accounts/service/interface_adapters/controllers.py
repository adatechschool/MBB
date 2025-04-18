# accounts/service/interface_adapters/controllers.py

"""Controller for handling account-related HTTP requests and responses."""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.service.application.use_cases import (
    GetAccount,
    UpdateAccount,
    DeleteAccount,
)
from accounts.service.infrastructure.django_account_repository import (
    DjangoAccountRepository,
)
from accounts.service.interface_adapters.presenters import AccountPresenter


USER_ID_REQUIRED = "User ID is required."


class AccountController(APIView):
    """Controller class that handles HTTP requests and responses for account-related operations."""

    permission_classes = [IsAuthenticated]
    repository = DjangoAccountRepository()

    def get(self, request, user_id=None):
        """Handle GET request to retrieve an account by user ID."""
        user_id = user_id or request.user.user_id

        use_case = GetAccount(self.repository)
        try:
            account = use_case.execute(user_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        presenter = AccountPresenter()
        return presenter.present(account)

    def put(self, request, user_id=None):
        """Handle PUT request to update an existing account."""
        user_id = user_id or request.user.user_id
        username = request.data.get("username")
        email = request.data.get("email")
        bio = request.data.get("bio", "")
        profile_picture = request.data.get("profile_picture")

        if not username or not email:
            return Response(
                {"error": "Username and email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = UpdateAccount(self.repository)
        account = use_case.execute(user_id, username, email, bio, profile_picture)

        presenter = AccountPresenter()
        return presenter.present(account)

    def delete(self, request, user_id=None):
        """Delete a user account."""
        user_id = user_id or request.user.user_id

        use_case = DeleteAccount(self.repository)
        try:
            use_case.execute(user_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        response = Response(
            {"message": "Account deleted successfully."},
            status=status.HTTP_200_OK,
        )
        # Also clear authentication cookies
        response.delete_cookie("accessToken", path="/")
        response.delete_cookie("refreshToken", path="/")

        return response
