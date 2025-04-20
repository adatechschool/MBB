# sessions\service\client.py

"""Client module for making HTTP requests to the Sessions microservice."""

import requests
from django.conf import settings

from common.dtos import SessionDTO
from common.events import publish_event


class SessionClient:
    """HTTP client for interacting with the Sessions microservice."""

    BASE_URL = settings.SESSIONS_SERVICE_URL.rstrip("/")
    TIMEOUT = 5

    def create_session(self, refresh_token: str) -> SessionDTO:
        """Create a new session using a refresh token.

        Args:
            refresh_token: The refresh token to authenticate with

        Returns:
            SessionDTO: The newly created session data

        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        resp = requests.post(
            f"{self.BASE_URL}/api/sessions/add/",
            cookies={"refresh_token": refresh_token},
            timeout=self.TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        publish_event(
            "session.created",
            {
                "session_id": data.get("session_id"),
                "expires_at": data.get("expires_at"),
            },
        )
        return SessionDTO(**data)

    def get_sessions(self, user_id: int) -> list[SessionDTO]:
        """Get all active sessions for a user.

        Args:
            user_id: The ID of the user to get sessions for

        Returns:
            list[SessionDTO]: List of active sessions for the user

        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        resp = requests.get(
            f"{self.BASE_URL}/api/sessions/current/",
            params={"user_id": user_id},
            timeout=self.TIMEOUT,
        )
        resp.raise_for_status()
        arr = resp.json()["data"]
        return [SessionDTO(**item) for item in arr]

    def refresh_session(self, old_refresh: str, new_refresh: str) -> None:
        """Refresh a session using the old refresh token.

        Args:
            old_refresh: The current refresh token to be replaced
            new_refresh: The new refresh token to be used

        Raises:
            requests.exceptions.HTTPError: If the request fails
        """
        resp = requests.post(
            f"{self.BASE_URL}/api/sessions/refresh/",
            cookies={"refresh_token": old_refresh},
            timeout=self.TIMEOUT,
        )
        resp.raise_for_status()
        publish_event(
            "session.refreshed",
            {"old_refresh": old_refresh, "new_refresh": new_refresh},
        )
