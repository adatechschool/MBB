from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  
from services.users.application.services import UserService
from services.users.infrastructure.repositories import UserRepository
from services.users.infrastructure.serializers import UserSerializer
from config.settings import DATABASES
# Exemple d'utilisation
db =DATABASES
# user_repository = UserRepository(db)
user_service = UserService(UserRepository(db))

class UserView(APIView):
    def get(self, request, user_id):
        user = user_service.get_user(user_id)
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = user_service.create_user(serializer.validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
