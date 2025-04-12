# services\users\interfaces\views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from services.users.application.services import UserService
from services.users.infrastructure.repositories import UserRepository
from services.users.infrastructure.serializers import UserUpdateSerializer


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    user_service = UserService(UserRepository())

    def get(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            updated_user = self.user_service.update_account(
                request.user, serializer.validated_data)
            updated_serializer = UserUpdateSerializer(updated_user)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = self.user_service.update_account(
                request.user, serializer.validated_data)
            updated_serializer = UserUpdateSerializer(updated_user)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        self.user_service.delete_account(request.user)
        return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)
