# sessions/service/application/repositories/session_repository.py

"""Defines the interface for session repository implementations."""

from abc import ABC, abstractmethod
from typing import Optional
from sessions.service.core.entities.session import SessionEntity


class SessionRepositoryInterface(ABC):
    """Abstract interface defining the contract for session repository implementations.

    This interface specifies the required methods that any concrete session repository
    must implement to handle session storage, retrieval, and deletion operations.
    """

    @abstractmethod
    def create_session(self, user_id: int, token: str, expires_at) -> SessionEntity:
        """Creates a new session and returns its entity."""

    @abstractmethod
    def get_session_by_id(self, session_id: int) -> Optional[SessionEntity]:
        """Retrieves a session based on its ID."""

    @abstractmethod
    def get_session_by_token(self, token: str) -> Optional[SessionEntity]:
        """Retrieves a session based on the token value."""

    @abstractmethod
    def delete_session(self, session_id: int) -> None:
        """Deletes a session specified by its ID."""
