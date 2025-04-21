# sessions\service\application\repositories.py

"""Repository interface for session management operations."""

from abc import ABC, abstractmethod
from typing import List

from sessions.service.domain.entities import SessionModel


class SessionRepositoryInterface(ABC):
    """Interface defining the contract for session management operations."""

    @abstractmethod
    def create_session(self, user_id: int, refresh_token: str) -> SessionModel:
        """Create and persist a new session record."""

    @abstractmethod
    def get_sessions(self, user_id: int) -> List[SessionModel]:
        """Retrieve all active sessions for a given user."""

    @abstractmethod
    def refresh_session(
        self, old_refresh_token: str, new_refresh_token: str
    ) -> SessionModel:
        """Update the session with a rotated refresh token."""
