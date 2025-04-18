# authentication\service\application\use_cases\create_session.py

"""Module containing the CreateSession use case for managing user sessions."""

from sessions.service.application.repositories.session_repository import (
    SessionRepositoryInterface,
)


class CreateSession:
    """Use case for creating new user sessions in the system.

    This class handles the creation of user sessions by interacting with a session repository.
    It takes a session repository as a dependency and provides an execute method to create sessions.
    """

    def __init__(self, session_repository: SessionRepositoryInterface):
        self.session_repository = session_repository

    def execute(self, user_id: int, token: str, expires_at):
        """Create a new session for a user.

        Args:
            user_id (int): The ID of the user
            token (str): The session token
            expires_at: The expiration timestamp

        Returns:
            The created session
        """
        return self.session_repository.create_session(user_id, token, expires_at)
