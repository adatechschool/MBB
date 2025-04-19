# sessions\service\application\use_cases.py

"""Use case layer for session operations."""

from typing import List

from sessions.service.application.repositories import SessionRepositoryInterface
from sessions.service.core.entities import SessionEntity


class SessionUseCase:
    """Use case class handling session management operations."""

    def __init__(self, repo: SessionRepositoryInterface):
        self.repo = repo

    def create_session(self, user_id: int, refresh_token: str) -> SessionEntity:
        """Create a new session for a user with the given refresh token.

        Args:
            user_id (int): The ID of the user creating the session
            refresh_token (str): The refresh token for the session

        Returns:
            SessionEntity: The newly created session entity
        """
        return self.repo.create_session(user_id, refresh_token)

    def get_current_sessions(self, user_id: int) -> List[SessionEntity]:
        """Get all current sessions for a user.

        Args:
            user_id (int): The ID of the user whose sessions to retrieve

        Returns:
            List[SessionEntity]: List of current session entities for the user
        """
        return self.repo.get_sessions(user_id)

    def refresh_session(
        self, old_refresh_token: str, new_refresh_token: str
    ) -> SessionEntity:
        """Refresh a session by replacing its refresh token.

        Args:
            old_refresh_token (str): The current refresh token of the session
            new_refresh_token (str): The new refresh token to replace the old one

        Returns:
            SessionEntity: The updated session entity
        """
        return self.repo.refresh_session(old_refresh_token, new_refresh_token)
