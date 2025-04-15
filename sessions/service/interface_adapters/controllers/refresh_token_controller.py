# sessions/service/interface_adapters/controllers/refresh_token_controller.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from service.application.repositories.django_session_repository import (
    DjangoSessionRepository,
)


class RefreshTokenController(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            # Validate the refresh token using SimpleJWT.
            token = RefreshToken(refresh_token)
        except TokenError:
            # Optionally, delete the session record if invalid.
            session_repository = DjangoSessionRepository()
            session_repository.delete_session_by_token(refresh_token)
            return Response(
                {"error": "Refresh token is expired or invalid. Please log in again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        session_repository = DjangoSessionRepository()
        session_entity = session_repository.get_session_by_token(refresh_token)
        if session_entity is None:
            return Response(
                {"error": "Session not found. Please log in again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Token is valid; generate a new access token.
        new_access_token = str(token.access_token)
        return Response({"access": new_access_token}, status=status.HTTP_200_OK)
