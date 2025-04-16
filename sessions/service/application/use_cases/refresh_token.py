# sessions/service/application/use_cases/refresh_token.py

import datetime
import jwt
from django.conf import settings
from service.application.repositories.session_repository import (
    SessionRepositoryInterface,
)


class RefreshToken:
    def __init__(self, session_repository: SessionRepositoryInterface):
        self.session_repository = session_repository

    def execute(self, session_id: int):
        # Retrieve the session from the repository
        session = self.session_repository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found.")

        # Check if the refresh token has expired
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        if session.expires_at < now:
            # Optionally: delete the session as it is no longer valid
            self.session_repository.delete_session(session_id)
            raise ValueError("Refresh token expired. Please log in again.")

        # Generate a new access token.
        # Adjust the payload and expiration as needed.
        payload = {
            "user_id": session.user_id,
            "exp": now + datetime.timedelta(minutes=10),
        }
        new_access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return new_access_token
