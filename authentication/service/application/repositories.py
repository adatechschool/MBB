# authentication\service\application\repositories.py

"""Repository interface for authentication operations."""

from abc import ABC, abstractmethod

from authentication.service.core.entities import AuthTokens


class AuthRepositoryInterface(ABC):
    """Interface for authentication-related persistence operations."""

    @abstractmethod
    def register(self, username: str, email: str, password: str) -> None:
        """Create a new user account"""

    @abstractmethod
    def authenticate(self, username: str, password: str) -> AuthTokens:
        """Validate credentials and return JWT tokens"""

    @abstractmethod
    def blacklist(self, refresh_token: str) -> None:
        """Blacklist a refresh token upon logout"""
