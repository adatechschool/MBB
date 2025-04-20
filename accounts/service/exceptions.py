# accounts/service/exceptions.py


class AccountNotFound(Exception):
    """Raised when an account does not exist in the repository."""


class AccountConflict(Exception):
    """Raised when attempting to create/update to a username/email that’s already taken."""
