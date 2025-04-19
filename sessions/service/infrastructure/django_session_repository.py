# sessions\service\infrastructure\django_session_repository.py

"""Django ORM implementation of the session repository interface."""

from datetime import datetime, timezone as dt_timezone
from rest_framework_simplejwt.tokens import RefreshToken

from sessions.service.application.repositories import SessionRepositoryInterface
from sessions.service.core.entities import SessionEntity
from sessions.service.models import SessionModel


class DjangoSessionRepository(SessionRepositoryInterface):
    """Django ORM implementation for managing user sessions in the database."""

    def create_session(self, user_id: int, refresh_token: str) -> SessionEntity:
        token_obj = RefreshToken(refresh_token)
        expires_ts = token_obj["exp"]
        expires_at = datetime.fromtimestamp(expires_ts, tz=dt_timezone.utc)
        session = SessionModel.objects.create(
            user_id=user_id,
            token=refresh_token,
            expires_at=expires_at,
        )
        return SessionEntity(
            session_id=session.session_id,
            user_id=session.user_id,
            token=session.token,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )

    def get_sessions(self, user_id: int) -> list[SessionEntity]:
        sessions = SessionModel.objects.filter(user_id=user_id)
        return [
            SessionEntity(
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
    ) -> SessionEntity:
        session = SessionModel.objects.get(token=old_refresh_token)
        token_obj = RefreshToken(new_refresh_token)
        expires_ts = token_obj["exp"]
        expires_at = datetime.fromtimestamp(expires_ts, tz=dt_timezone.utc)
        session.token = new_refresh_token
        session.expires_at = expires_at
        session.save(update_fields=["token", "expires_at"])
        return SessionEntity(
            session_id=session.session_id,
            user_id=session.user_id,
            token=session.token,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )
