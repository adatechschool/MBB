# accounts/service/interface_adapters/controllers.py

"""Controller for account-related HTTP requests and responses."""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from accounts.service.application.use_cases import AccountUseCase
from accounts.service.interface_adapters.presenters import AccountPresenter
from accounts.service.models import AccountModel
from accounts.service.infrastructure.django_account_repository import (
    DjangoAccountRepository,
)


class AccountController(APIView):
    """Controller for account endpoints."""

    permission_classes = [IsAuthenticated]
    use_case = AccountUseCase(DjangoAccountRepository())
    presenter = AccountPresenter()

    def get(self, request):
        """Retrieve account information for the authenticated user.

        Args:
            request: HTTP request object containing user authentication.

        Returns:
            Response object with account data or not found error.
        """
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        entity = self.use_case.get_account(user_id)
        if not entity:
            return self.presenter.present_not_found()
        return self.presenter.present_account(entity)

    def put(self, request):
        """Update account information for the authenticated user.

        Args:
            request: HTTP request object containing user authentication and update data.

        Returns:
            Response object with updated account data or not found error.
        """
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        data = request.data
        try:
            updated = self.use_case.update_account(
                user_id,
                data.get("username"),
                data.get("email"),
                data.get("bio"),
                data.get("profile_picture"),
            )
        except AccountModel.DoesNotExist:
            return self.presenter.present_not_found()
        return self.presenter.present_account(updated)

    def delete(self, request):
        """Delete account for the authenticated user.

        Args:
            request: HTTP request object containing user authentication.

        Returns:
            Response object confirming account deletion.
        """
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        self.use_case.delete_account(user_id)
        return self.presenter.present_deleted()
