# sessions/service/application/use_cases/get_session.py

"""Use case for retrieving a session by its ID."""

from sessions.service.application.repositories.session_repository import (
    SessionRepositoryInterface,
)


class GetSession:
    """Use case for retrieving a session from the repository by its ID.

    Args:
        session_repository: Repository interface for session operations.
    """

    def __init__(self, session_repository: SessionRepositoryInterface):
        self.session_repository = session_repository

    def execute(self, session_id: int):
        """Retrieve a session by its ID.

        Args:
            session_id: The ID of the session to retrieve.

        Returns:
            The session object if found.

        Raises:
            ValueError: If the session is not found.
        """
        session = self.session_repository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found")
        return session
