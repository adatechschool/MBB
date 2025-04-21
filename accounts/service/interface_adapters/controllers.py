# accounts\service\interface_adapters\controllers.py

"""Controller for account-related HTTP requests and responses."""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from common.events import publish_event
from accounts.service.application.use_cases import AccountUseCase
from accounts.service.interface_adapters.presenters import AccountPresenter
from accounts.service.infrastructure.django_account_repository import (
    DjangoAccountRepository,
)
from accounts.service.exceptions import AccountNotFound, AccountConflict


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
        try:
            entity = self.use_case.get_account(user_id)
        except AccountNotFound as exc:
            return self.presenter.present_error(
                str(exc), code=status.HTTP_404_NOT_FOUND
            )
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
        except AccountNotFound:
            return self.presenter.present_not_found()
        except AccountConflict as exc:
            return self.presenter.present_error(str(exc), code=status.HTTP_409_CONFLICT)
        entity = updated
        publish_event("account.updated", entity.to_dict())
        return self.presenter.present_account(updated)

    def delete(self, request):
        """Delete account for the authenticated user.

        Args:
            request: HTTP request object containing user authentication.

        Returns:
            Response object confirming account deletion.
        """
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        try:
            self.use_case.delete_account(user_id)
        except AccountNotFound:
            return self.presenter.present_not_found()
        publish_event("account.deleted", {"user_id": user_id})
        return self.presenter.present_deleted()
