# sessions/service/application/use_cases/delete_session.py

"""Use case for deleting a user session."""

from service.application.repositories.session_repository import (
    SessionRepositoryInterface,
)


class DeleteSession:
    """Use case for deleting a user session from the repository."""

    def __init__(self, session_repository: SessionRepositoryInterface):
        self.session_repository = session_repository

    def execute(self, session_id: int):
        """Delete a session from the repository.

        Args:
            session_id: The ID of the session to delete.

        Returns:
            The deleted session object.

        Raises:
            ValueError: If the session is not found.
        """
        session = self.session_repository.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Session not found")
        self.session_repository.delete_session(session_id)
        return session
