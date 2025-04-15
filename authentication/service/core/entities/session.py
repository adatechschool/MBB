# authentication\service\core\entities\session.py

"""Module containing the SessionEntity class for representing user sessions."""


class SessionEntity:
    """Represents a user session with authentication token and expiry information."""

    def __init__(
        self, session_id: int, user_id: int, token: str, created_at, expires_at
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.token = token
        self.created_at = created_at
        self.expires_at = expires_at

    def __repr__(self):
        return (
            f"<SessionEntity id={self.session_id} user_id={self.user_id} "
            f"token={self.token} created_at={self.created_at} expires_at={self.expires_at}>"
        )
