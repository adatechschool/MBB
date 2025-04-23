# users\service\interface_adapters\controllers.py

"""Controller for user-related HTTP requests and responses."""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.service.application.use_cases import UserUseCase
from users.service.infrastructure.django_user_repository import DjangoUserRepository


class UsersController(APIView):
    """Controller for listing all users without authentication"""
    permission_classes = [AllowAny]

    permission_classes = [AllowAny]
    use_case = UserUseCase(DjangoUserRepository())

    def get(self, request):
        """
        Retrieve all users.
        """
        dtos = self.use_case.get_all_users()
        payload = [dto.to_dict() for dto in dtos]
        return Response(
            {"status": "success", "data": payload, "error": None},
            status=status.HTTP_200_OK,
    )
