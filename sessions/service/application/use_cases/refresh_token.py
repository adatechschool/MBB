# sessions/service/application/use_cases/refresh_token.py

"""Module for handling authentication token refresh operations."""

import datetime
import jwt
from django.conf import settings
from service.application.repositories.session_repository import (
    SessionRepositoryInterface,
)


class RefreshToken:
    """Use case for refreshing an authentication token using a valid session."""

    def __init__(self, session_repository: SessionRepositoryInterface):
        self.session_repository = session_repository

    def execute(self, session_id: int):
        """Generate a new access token for a valid session.

        Args:
            session_id: The ID of the session to refresh

        Returns:
            str: A new JWT access token

        Raises:
            ValueError: If session is not found or refresh token has expired
        """
        session = self.session_repository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found.")

        now = datetime.datetime.now(datetime.timezone.utc)
        if session.expires_at < now:
            self.session_repository.delete_session(session_id)
            raise ValueError("Refresh token expired. Please log in again.")

        payload = {
            "user_id": session.user_id,
            "exp": now + datetime.timedelta(minutes=10),
        }
        new_access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return new_access_token
