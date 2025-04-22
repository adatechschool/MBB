# authentication\service\domain\entities.py

"""Domain entity representing JWT auth tokens."""

from dataclasses import dataclass


@dataclass
class AuthModel:
    """Domain entity representing JWT auth tokens."""

    access: str
    refresh: str
