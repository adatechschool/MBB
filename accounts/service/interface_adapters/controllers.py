# accounts\service\interface_adapters\controllers.py

"""Controller for account-related HTTP requests and responses."""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.events import publish_event
from accounts.service.application.use_cases import AccountUseCase
from accounts.service.infrastructure.django_account_repository import (
    DjangoAccountRepository,
)
from accounts.service.exceptions import AccountNotFound, AccountConflict


class AccountController(APIView):
    """Controller for account endpoints."""

    permission_classes = [IsAuthenticated]
    use_case = AccountUseCase(DjangoAccountRepository())

    def get(self, request):
        """Retrieve account information for the authenticated user.

        Args:
            request: HTTP request object containing user authentication.

        Returns:
            Response object with account data or not found error.
        """
        print("COOKIES: ", request.COOKIES)
        print("AUTH HEADER: ", request.META.get("HTTP_AUTHORIZATION"))
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        try:
            dto = self.use_case.get_account(user_id)
        except AccountNotFound as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"code": status.HTTP_404_NOT_FOUND, "message": str(exc)},
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"status": "success", "data": dto.to_dict(), "error": None},
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        """
        Update account information for the authenticated user.

        Args:
            request: HTTP request object containing user authentication and update data.

        Returns:
            Response object with updated account data or not found error.
        """
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        data = request.data
        try:
            dto = self.use_case.update_account(
                user_id,
                data.get("username"),
                data.get("email"),
                data.get("bio"),
                data.get("profile_picture"),
            )
        except AccountNotFound as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"code": status.HTTP_404_NOT_FOUND, "message": str(exc)},
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except AccountConflict as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"code": status.HTTP_409_CONFLICT, "message": str(exc)},
                },
                status=status.HTTP_409_CONFLICT,
            )
        publish_event("account.updated", dto.to_dict())
        return Response(
            {"status": "success", "data": dto.to_dict(), "error": None},
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        """
        Delete account for the authenticated user.

        Args:
            request: HTTP request object containing user authentication.

        Returns:
            Response object confirming account deletion.
        """
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        try:
            self.use_case.delete_account(user_id)
        except AccountNotFound as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"code": status.HTTP_404_NOT_FOUND, "message": str(exc)},
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        publish_event("account.deleted", {"user_id": user_id})
        return Response(
            {"status": "success", "data": {}, "error": None},
            status=status.HTTP_204_NO_CONTENT,
        )
