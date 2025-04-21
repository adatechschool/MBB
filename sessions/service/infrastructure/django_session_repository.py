# sessions\service\infrastructure\django_session_repository.py

"""Django ORM implementation of the session repository interface."""

from datetime import datetime, timezone as dt_timezone
from rest_framework_simplejwt.tokens import RefreshToken

from sessions.service.application.repositories import SessionRepositoryInterface
from sessions.service.domain.entities import SessionModel
from sessions.service.exceptions import (
    SessionCreateError,
    SessionNotFound,
    SessionRefreshError,
)
from common.dtos import SessionDTO


class DjangoSessionRepository(SessionRepositoryInterface):
    """Django ORM implementation for managing user sessions in the database."""

    def create_session(self, user_id: int, refresh_token: str) -> SessionDTO:
        token_obj = RefreshToken(refresh_token)
        expires_ts = token_obj["exp"]
        expires_at = datetime.fromtimestamp(expires_ts, tz=dt_timezone.utc)
        try:
            session = SessionModel.objects.create(
                user_id=user_id,
                token=refresh_token,
                expires_at=expires_at,
            )
        except Exception as exc:
            raise SessionCreateError("Session creation failed.") from exc
        return SessionDTO(
            session_id=session.session_id,
            user_id=session.user_id,
            token=session.token,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )

    def get_sessions(self, user_id: int) -> list[SessionDTO]:
        sessions = SessionModel.objects.filter(user_id=user_id)
        if not sessions:
            raise SessionNotFound("Session not found.")
        return [
            SessionDTO(
                session_id=s.session_id,
                user_id=s.user_id,
                token=s.token,
                created_at=s.created_at,
                expires_at=s.expires_at,
            )
            for s in sessions
        ]

    def refresh_session(
        self, old_refresh_token: str, new_refresh_token: str
    ) -> SessionDTO:
        session = SessionModel.objects.get(token=old_refresh_token)
        token_obj = RefreshToken(new_refresh_token)
        expires_ts = token_obj["exp"]
        expires_at = datetime.fromtimestamp(expires_ts, tz=dt_timezone.utc)
        session.token = new_refresh_token
        session.expires_at = expires_at
        try:
            session.save(update_fields=["token", "expires_at"])
        except Exception as exc:
            raise SessionRefreshError("Session refresh failed.") from exc
        return SessionDTO(
            session_id=session.session_id,
            user_id=session.user_id,
            token=session.token,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )
