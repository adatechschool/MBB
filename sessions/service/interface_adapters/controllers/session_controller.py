# sessions/service/interface_adapters/controllers/session_controller.py

"""
Controller module for handling HTTP requests related to session management.
Provides endpoints for creating, retrieving and deleting sessions.
"""

from dateutil.parser import parse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service.application.repositories.django_session_repository import (
    DjangoSessionRepository,
)
from service.application.use_cases.create_session import CreateSession
from service.application.use_cases.get_session import GetSession
from service.application.use_cases.delete_session import DeleteSession
from service.interface_adapters.presenters.session_presenter import SessionPresenter


class SessionController(APIView):
    """
    API view for managing sessions.

    Endpoints:
      - POST /api/sessions/ : Create a new session.
      - GET  /api/sessions/ or /api/sessions/current/ : Get current session via Bearer token.
      - GET  /api/sessions/<int:session_id>/ : Retrieve a session by its ID.
      - DELETE /api/sessions/<int:session_id>/ : Delete a session.
    """

    def post(self, request):
        """
        Create a new session with the provided user_id, token and expires_at.

        Args:
            request: HTTP request containing user_id, token and expires_at in the request data

        Returns:
            Response: HTTP response with the created session data or error message
        """
        user_id = request.data.get("user_id")
        token = request.data.get("token")
        expires_at = request.data.get("expires_at")

        if not user_id or not token or not expires_at:
            return Response(
                {"error": "user_id, token and expires_at are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            expires_at = parse(expires_at)

        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid expires_at format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session_repository = DjangoSessionRepository()
        use_case = CreateSession(session_repository)
        session_entity = use_case.execute(user_id, token, expires_at)

        presenter = SessionPresenter()
        return presenter.present(session_entity)

    def get(self, request, session_id=None):
        """
        Retrieve a session either by session ID or Bearer token.

        Args:
                request: The HTTP request object
                session_id: Optional session ID from the URL

        Returns:
                Response containing the session data or an error message
        """
        session_repository = DjangoSessionRepository()
        presenter = SessionPresenter()

        # If a session_id is provided in the URL, retrieve that specific session
        if session_id is not None:
            use_case = GetSession(session_repository)
            try:
                session_entity = use_case.execute(session_id)
                return presenter.present(session_entity)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Otherwise, attempt to get the current session using the Bearer token from the header
            auth_header = request.META.get("HTTP_AUTHORIZATION", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.split("Bearer ")[1]
                session_entity = session_repository.get_session_by_token(token)
                if session_entity is None:
                    return Response(
                        {"error": "Session not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                return presenter.present(session_entity)
            return Response(
                {"error": "Either session ID or Bearer token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, session_id=None):
        """Delete a session by its ID.

        Args:
            request: The HTTP request object
            session_id: The ID of the session to delete

        Returns:
            Response: HTTP response indicating success or failure
        """
        if not session_id:
            return Response(
                {"error": "Session ID is required for deletion."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        session_repository = DjangoSessionRepository()
        use_case = DeleteSession(session_repository)
        try:
            use_case.execute(session_id)
            return Response(
                {"message": "Session deleted successfully"}, status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
