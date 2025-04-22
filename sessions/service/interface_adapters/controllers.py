# sessions\service\interface_adapters\controllers.py

"""Controller for session-related HTTP requests and responses."""

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from sessions.service.application.use_cases import SessionUseCase
from sessions.service.infrastructure.django_session_repository import (
    DjangoSessionRepository,
)
from sessions.service.exceptions import (
    SessionCreateError,
    SessionNotFound,
    SessionRefreshError,
)

COOKIE_PATH = "/"
ACCESS_COOKIE_AGE = int(getattr(settings, "SIMPLE_JWT", {}).get("ACCESS_TOKEN_LIFETIME").total_seconds())
REFRESH_COOKIE_AGE = int(getattr(settings, "SIMPLE_JWT", {}).get("REFRESH_TOKEN_LIFETIME").total_seconds())


class SessionController(APIView):
    """Controller for managing user sessions through HTTP endpoints.

    Handles creation and retrieval of user sessions with authentication requirements.
    Uses SessionUseCase for business logic and SessionPresenter for response formatting.
    """

    permission_classes = [IsAuthenticated]
    use_case = SessionUseCase(DjangoSessionRepository())

    def post(self, request):
        """Create a new session for an authenticated user.

        Args:
            request: HTTP request containing user authentication and refresh token cookie.

        Returns:
            Response with created session details or error message.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "message": "Refresh token not provided.",
                    },
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        try:
            dto = self.use_case.create_session(user_id, refresh_token)
        except SessionCreateError as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"code": status.HTTP_400_BAD_REQUEST, "message": str(exc)},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"status": "success", "data": dto.to_dict(), "error": None},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        """Get all current sessions for an authenticated user.

        Args:
            request: HTTP request containing user authentication.

        Returns:
            Response with list of active sessions for the user.
        """
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        try:
            dtos = self.use_case.get_current_sessions(user_id)
        except SessionNotFound as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"code": status.HTTP_404_NOT_FOUND, "message": str(exc)},
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {
                "status": "success",
                "data": [dto.to_dict() for dto in dtos],
                "error": None,
            },
            status=status.HTTP_200_OK,
        )


@method_decorator(csrf_exempt, name="dispatch")
class CookieTokenRefreshView(APIView):
    """Handle token refresh operations using HTTP cookies.

    This view accepts refresh tokens from cookies and returns new access/refresh tokens,
    maintaining session state and cookie-based token storage.
    """

    permission_classes = [AllowAny]
    use_case = SessionUseCase(DjangoSessionRepository())

    def post(self, request):
        """Handle refresh token rotation and access token renewal.

        Args:
            request: HTTP request containing refresh token in cookies.

        Returns:
            Response with new access token and optionally rotated refresh token.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "message": "Refresh token not provided.",
                    },
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
            serializer.is_valid(raise_exception=True)
            access = serializer.validated_data["access"]
            new_refresh = serializer.validated_data.get("refresh")
            RefreshToken(refresh_token).blacklist()
            if new_refresh:
                self.use_case.refresh_session(refresh_token, new_refresh)
                refresh_value = new_refresh
            else:
                refresh_value = refresh_token
        except TokenError as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "message": str(exc),
                    },
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except SessionRefreshError as exc:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": str(exc),
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        response = Response(
            {
                "status": "success",
                "data": {"access": access, "refresh": refresh_value},
                "error": None,
            },
            status=status.HTTP_200_OK,
        )
        secure_flag = not settings.DEBUG
        response.set_cookie(
            key="access_token",
            value=access,
            max_age=ACCESS_COOKIE_AGE,
            httponly=True,
            secure=secure_flag,
            samesite="Lax",
            path=COOKIE_PATH,
        )
        response.set_cookie(
            key="access_token",
            value=access,
            max_age=ACCESS_COOKIE_AGE,
            httponly=True,
            secure=secure_flag,
            samesite="Lax",
            path=COOKIE_PATH,
        )
        return response
