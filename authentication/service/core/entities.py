# authentication/service/core/entities.py

"""Domain entity representing JWT auth tokens."""

from dataclasses import dataclass


@dataclass
class AuthTokens:
    """Domain entity representing JWT auth tokens."""

    access: str
    refresh: str
