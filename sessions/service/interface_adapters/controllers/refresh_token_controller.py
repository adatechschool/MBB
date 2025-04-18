# pylint: skip-file
# sessions/service/interface_adapters/controllers/refresh_token_controller.py

"""Controller for handling refresh token operations."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from service.application.use_cases.refresh_token import RefreshToken
from microblog_common.session_repository import DjangoSessionRepository


class RefreshTokenController(APIView):
    """Controller handling refresh token operations for user sessions.

    Provides endpoint to refresh expired access tokens using valid session IDs.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST requests to refresh access tokens.

        Args:
            request: HTTP request containing session_id in request data

        Returns:
            Response with new access token or error message
        """
        # pull the raw refresh token straight from the cookie
        raw_refresh = request.COOKIES.get("refreshToken")
        if not raw_refresh:
            return Response(
                {"error": "Refresh token cookie is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # look up the session by its token
        session_repo = DjangoSessionRepository()
        session = session_repo.get_session_by_token(raw_refresh)
        if session is None:
            return Response(
                {"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # now use the use case
        use_case = RefreshToken(session_repo)
        try:
            new_access = use_case.execute(session.session_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # respond and rotate the accessToken cookie
        resp = Response({"access": new_access}, status=status.HTTP_200_OK)
        resp.set_cookie(
            key="accessToken",
            value=new_access,
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        return resp
