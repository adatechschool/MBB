# sessions/service/interface_adapters/presenters/session_presenter.py

"""Presenter module for formatting session responses."""

from rest_framework.response import Response


class SessionPresenter:
    """Presenter class responsible for formatting session data into HTTP responses."""

    def present(self, session_entity):
        """Format session entity into HTTP response.

        Args:
            session_entity: Session entity containing session data

        Returns:
            Response: HTTP response containing formatted session data
        """
        return Response(
            {
                "session_id": session_entity.session_id,
                "user_id": session_entity.user_id,
                "token": session_entity.token,
                "created_at": session_entity.created_at,
                "expires_at": session_entity.expires_at,
            },
            status=200,
        )
