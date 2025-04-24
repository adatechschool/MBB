# authentication\service\client.py

"""Authentication service client module for making HTTP requests to the Auth microservice."""

import requests
from django.conf import settings

from common.dtos import AuthDTO
from common.events import publish_event


class AuthClient:
    """HTTP client for interacting with the Authentication microservice."""

    BASE_URL = settings.AUTH_SERVICE_URL.rstrip("/")

    def register(self, username: str, email: str, password: str) -> int:
        """Register a new user with the authentication service.

        Args:
            username: The username for the new user
            email: The email address for the new user
            password: The password for the new user

        Returns:
            int: The ID of the newly created user
        """
        resp = requests.post(
            f"{self.BASE_URL}/api/auth/register/",
            json={"username": username, "email": email, "password": password},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        publish_event(
            "user.registered",
            {"user_id": data.get("user_id"), "username": username, "email": email},
        )
        return data.get("user_id")

    def login(self, email: str, password: str) -> AuthDTO:
        """Authenticate a user with their credentials.

        Args:
            username: The username of the user trying to login
            password: The password of the user trying to login

        Returns:
            AuthDTO: Data transfer object containing access and refresh tokens
        """
        resp = requests.post(
            f"{self.BASE_URL}/api/auth/login/",
            json={"email": email, "password": password},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        publish_event("user.logged_in", {"email": email})
        return AuthDTO(access=data["access"], refresh=data["refresh"])

    def logout(self, refresh_token: str) -> None:
        """Logout a user by invalidating their refresh token.

        Args:
            refresh_token: The refresh token to invalidate

        Returns:
            None
        """
        resp = requests.post(f"{self.BASE_URL}/api/auth/logout/", timeout=30)
        resp.raise_for_status()
        publish_event("user.logged_out", {"refresh_token": refresh_token})
