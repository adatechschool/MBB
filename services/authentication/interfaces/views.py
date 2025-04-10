# services/authentication/interfaces/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # Import this
from services.authentication.application.services import AuthService
from services.authentication.infrastructure.repositories import AuthRepository
from services.authentication.infrastructure.serializers import LoginSerializer, RegisterSerializer, SessionSerializer

# Instantiate the service with its repository
auth_service = AuthService(AuthRepository())


class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = auth_service.register_user(
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password'],
                    email=serializer.validated_data.get('email')
                )
                return Response({
                    "message": "User registered successfully.",
                    "username": user.username
                }, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                session = auth_service.login_user(
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password']
                )
                session_serializer = SessionSerializer(session)
                return Response(session_serializer.data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # Typically, logout may require a valid token.
    # You can choose to require authentication or override with AllowAny if needed.
    # For now, if you want to allow token-based access without CSRF issues, you might leave it as is
    # or explicitly set an authentication class accordingly.
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[-1]
            if auth_service.logout_user(token):
                return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Authorization token not provided."}, status=status.HTTP_400_BAD_REQUEST)
