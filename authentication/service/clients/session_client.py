# authentication\service\clients\session_client.py

import requests
from django.conf import settings
from common.dtos import SessionDTO


class SessionServiceClient:
    def __init__(self):
        self.base_url = (
            settings.SESSIONS_SERVICE_URL
        )  # e.g. "https://sessions.example.com"

    def create(self, user_id: int, token: str, expires_at) -> SessionDTO:
        resp = requests.post(
            f"{self.base_url}/api/sessions/add/",
            json={
                "user_id": user_id,
                "token": token,
                "expires_at": expires_at.isoformat(),
            },
            timeout=2,
        )
        resp.raise_for_status()
        return SessionDTO(**resp.json())
