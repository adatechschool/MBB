# microblog_common/session_repository.py

"""
Repository implementation for managing user sessions using Django's session framework.
Provides methods for CRUD operations on user sessions.
"""

from typing import Optional
from importlib import import_module
from django.conf import settings
from sessions.service.core.entities.session import SessionEntity


class DjangoSessionRepository:
    """
    Shared Django implementation of SessionRepositoryInterface.
    Expects your consumer to have a `Session` model in INSTALLED_APPS
    at settings.AUTH_SESSION_MODEL (default "service.Session").
    """

    def __init__(self, session_model_path: Optional[str] = None):
        """
        Args:
            session_model_path: Django app.model path, e.g. "service.Session".
                Falls back to settings.AUTH_SESSION_MODEL or "service.Session".
        """
        path = str(
            session_model_path
            or getattr(settings, "AUTH_SESSION_MODEL", "service.Session")  # noqa
        )
        app_label, model_name = path.split(".")
        self.session_model = import_module(f"{app_label}.models").__dict__[model_name]

    def create_session(self, user_id: int, token: str, expires_at) -> SessionEntity:
        """
        Creates a new session for the given user.

        Args:
            user_id: ID of the user to create session for
            token: Session authentication token
            expires_at: Session expiration timestamp

        Returns:
            SessionEntity: The created session entity
        """
        session = self.session_model.objects.create(
            user_id=user_id, token=token, expires_at=expires_at
        )
        return SessionEntity(
            session_id=session.session_id,
            user_id=session.pk,
            token=session.token,
            created_at=session.created_at,
            expires_at=session.expires_at,
        )

    def get_session_by_id(self, session_id: int) -> Optional[SessionEntity]:
        """
        Retrieves a session by its ID.

        Args:
            session_id: ID of the session to retrieve

        Returns:
            SessionEntity: The session entity if found, None otherwise
        """
        try:
            session = self.session_model.objects.get(session_id=session_id)
            return SessionEntity(
                session_id=session.session_id,
                user_id=session.pk,
                token=session.token,
                created_at=session.created_at,
                expires_at=session.expires_at,
            )
        except self.session_model.DoesNotExist:
            return None

    def get_session_by_token(self, token: str) -> Optional[SessionEntity]:
        """
        Retrieves a session by its token.

        Args:
            token: The token string to search for

        Returns:
            SessionEntity: The session entity if found, None otherwise
        """
        try:
            session = self.session_model.objects.get(token=token)
            return SessionEntity(
                session_id=session.session_id,
                user_id=session.pk,
                token=session.token,
                created_at=session.created_at,
                expires_at=session.expires_at,
            )
        except self.session_model.DoesNotExist:
            return None

    def delete_session(self, session_id: int) -> None:
        """
        Deletes a session by its ID.

        Args:
            session_id: The ID of the session to delete
        """
        self.session_model.objects.filter(session_id=session_id).delete()

    def delete_session_by_token(self, token: str) -> None:
        """
        Deletes a session by its token.

        Args:
            token: The token of the session to delete
        """
        self.session_model.objects.filter(token=token).delete()
