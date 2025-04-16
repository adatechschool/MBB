# sessions\service\application\repositories\django_session_repository.py
# pylint: disable=no-member

"""Django implementation of the session repository interface."""

from typing import Optional
from service.application.repositories.session_repository import (
    SessionRepositoryInterface,
)
from service.core.entities.session import SessionEntity
from service.models import Session


class DjangoSessionRepository(SessionRepositoryInterface):
    """Django implementation of the session repository for managing user sessions in the database"""

    def create_session(self, user_id: int, token: str, expires_at) -> SessionEntity:
        """Creates a new session in the database.

        Args:
            user_id (int): The ID of the user the session belongs to
            token (str): The session token
            expires_at: The expiration timestamp for the session

        Returns:
            SessionEntity: The created session entity
        """
        session = Session.objects.create(
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
        """Retrieves a session from the database by its ID.

        Args:
            session_id (int): The ID of the session to retrieve

        Returns:
            Optional[SessionEntity]: The session entity if found, None otherwise
        """
        try:
            session = Session.objects.get(session_id=session_id)
            return SessionEntity(
                session_id=session.session_id,
                user_id=session.pk,
                token=session.token,
                created_at=session.created_at,
                expires_at=session.expires_at,
            )
        except Session.DoesNotExist:
            return None

    def get_session_by_token(self, token: str) -> Optional[SessionEntity]:
        """Retrieves a session from the database by its ID.

        Args:
            session_id (int): The ID of the session to retrieve

        Returns:
            Optional[SessionEntity]: The session entity if found, None otherwise
        """
        try:
            session = Session.objects.get(token=token)
            return SessionEntity(
                session_id=session.session_id,
                user_id=session.pk,
                token=session.token,
                created_at=session.created_at,
                expires_at=session.expires_at,
            )
        except Session.DoesNotExist:
            return None

    def delete_session(self, session_id: int) -> None:
        """Retrieves a session from the database by its ID.

        Args:
            session_id (int): The ID of the session to retrieve

        Returns:
            Optional[SessionEntity]: The session entity if found, None otherwise
        """
        Session.objects.filter(session_id=session_id).delete()

    def delete_session_by_token(self, token: str) -> None:
        """Deletes a session from the database by its token.

        Args:
            token (str): The token of the session to delete

        Returns:
            None
        """
        Session.objects.filter(token=token).delete()
