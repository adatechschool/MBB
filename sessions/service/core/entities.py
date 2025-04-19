# sessions\service\core\entities.py

"""Domain entity representing a user session."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class SessionEntity:
    """Entity representing a user authentication session with its associated metadata."""

    session_id: int
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime
