# sessions\service\exceptions.py

"""Contains custom exceptions for the sessions service."""


class SessionNotFound(Exception):
    """Raised when a session cannot be found in the repository."""


class SessionCreateError(Exception):
    """Raised when session creation fails (e.g. invalid token)."""


class SessionRefreshError(Exception):
    """Raised when session refresh (token rotation) fails."""
