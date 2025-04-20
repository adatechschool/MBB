# authentication/service/core/exceptions.py


class UserAlreadyExists(Exception):
    """Raised when trying to register a user with a username or email that’s already taken."""


class AuthenticationFailed(Exception):
    """Raised when login credentials are invalid."""


class TokenBlacklistError(Exception):
    """Raised when trying to blacklist an invalid or expired refresh token."""
