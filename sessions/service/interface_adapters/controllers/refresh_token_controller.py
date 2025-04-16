# sessions/service/interface_adapters/controllers/refresh_token_controller.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.application.repositories.django_session_repository import (
    DjangoSessionRepository,
)
from service.application.use_cases.refresh_token import RefreshToken


class RefreshTokenController(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        if not session_id:
            return Response(
                {"error": "session_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            session_id = int(session_id)
        except ValueError:
            return Response(
                {"error": "Invalid session_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session_repository = DjangoSessionRepository()
        use_case = RefreshToken(session_repository)
        try:
            new_access_token = use_case.execute(session_id)
            return Response({"access": new_access_token}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
