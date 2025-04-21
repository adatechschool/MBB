# authentication\service\application\repositories.py

"""Repository interface for authentication operations."""

from abc import ABC, abstractmethod

from authentication.service.domain.entities import AuthModel


class AuthRepositoryInterface(ABC):
    """Interface for authentication-related persistence operations."""

    @abstractmethod
    def register(self, username: str, email: str, password: str) -> None:
        """Create a new user account"""

    @abstractmethod
    def authenticate(self, username: str, password: str) -> AuthModel:
        """Validate credentials and return JWT tokens"""

    @abstractmethod
    def blacklist(self, refresh_token: str) -> None:
        """Blacklist a refresh token upon logout"""
