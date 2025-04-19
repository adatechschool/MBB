# sessions\service\interface_adapters\presenters.py

"""Presenter for formatting session HTTP responses."""

from common.presenters import BasePresenter


class SessionPresenter(BasePresenter):
    """Presenter class that handles formatting of session-related responses."""

    def present_session_created(self, entity):
        """Format response for a newly created session.

        Args:
            entity: Session entity containing session details

        Returns:
            Dict containing formatted session data with 201 status code
        """
        return self.success(
            {
                "session_id": entity.session_id,
                "created_at": entity.created_at.isoformat(),
                "expires_at": entity.expires_at.isoformat(),
            },
            http_status=201,
        )

    def present_sessions(self, entities):
        """Format response for a list of sessions.

        Args:
            entities: List of Session entities containing session details

        Returns:
            Dict containing list of formatted session data
        """
        return self.success(
            [
                {
                    "session_id": e.session_id,
                    "created_at": e.created_at.isoformat(),
                    "expires_at": e.expires_at.isoformat(),
                }
                for e in entities
            ]
        )

    def present_refresh(self, access, refresh):
        """Format response for token refresh.

        Args:
            access: New access token string
            refresh: New refresh token string

        Returns:
            Dict containing new access and refresh tokens
        """
        return self.success({"access": access, "refresh": refresh})

    def present_error(self, message: str, code: int = 400):
        """Format error response with provided message and code."""
        return self.error(message, code)
