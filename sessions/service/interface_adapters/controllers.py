# sessions\service\interface_adapters\controllers.py

"""Controller for session-related HTTP requests and responses."""

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.conf import settings

from sessions.service.application.use_cases import SessionUseCase
from sessions.service.infrastructure.django_session_repository import (
    DjangoSessionRepository,
)
from sessions.service.interface_adapters.presenters import SessionPresenter


class SessionController(APIView):
    """Controller for managing user sessions through HTTP endpoints.

    Handles creation and retrieval of user sessions with authentication requirements.
    Uses SessionUseCase for business logic and SessionPresenter for response formatting.
    """

    permission_classes = [IsAuthenticated]
    use_case = SessionUseCase(DjangoSessionRepository())
    presenter = SessionPresenter()

    def post(self, request):
        """Create a new session for an authenticated user.

        Args:
            request: HTTP request containing user authentication and refresh token cookie.

        Returns:
            Response with created session details or error message.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return self.presenter.present_error(
                "Refresh token not provided.", code=status.HTTP_401_UNAUTHORIZED
            )
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        try:
            entity = self.use_case.create_session(user_id, refresh_token)
        except ValueError as exc:
            return self.presenter.present_error(str(exc))
        return self.presenter.present_session_created(entity)

    def get(self, request):
        """Get all current sessions for an authenticated user.

        Args:
            request: HTTP request containing user authentication.

        Returns:
            Response with list of active sessions for the user.
        """
        user_id = getattr(request.user, "user_id", None) or getattr(request.user, "id")
        entities = self.use_case.get_current_sessions(user_id)
        return self.presenter.present_sessions(entities)


class CookieTokenRefreshView(APIView):
    """Handle token refresh operations using HTTP cookies.

    This view accepts refresh tokens from cookies and returns new access/refresh tokens,
    maintaining session state and cookie-based token storage.
    """

    permission_classes = [AllowAny]
    use_case = SessionUseCase(DjangoSessionRepository())
    presenter = SessionPresenter()

    def post(self, request):
        """Handle refresh token rotation and access token renewal.

        Args:
            request: HTTP request containing refresh token in cookies.

        Returns:
            Response with new access token and optionally rotated refresh token.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return self.presenter.present_error(
                "Refresh token not provided.", code=status.HTTP_401_UNAUTHORIZED
            )
        try:
            serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
            serializer.is_valid(raise_exception=True)
            access = serializer.validated_data["access"]
            new_refresh = serializer.validated_data.get("refresh")
            # update session record if token rotated
            if new_refresh:
                self.use_case.refresh_session(refresh_token, new_refresh)
                refresh_value = new_refresh
            else:
                refresh_value = refresh_token
        except ValueError as exc:
            return self.presenter.present_error(str(exc))
        response = self.presenter.present_refresh(access, refresh_value)
        secure = not settings.DEBUG
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=secure,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_value,
            httponly=True,
            secure=secure,
            samesite="Lax",
        )
        return response
