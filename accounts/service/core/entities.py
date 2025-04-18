# accounts\service\core\entities.py

import base64
from datetime import datetime
from typing import Optional


class AccountEntity:
    """Represents a user account entity in the system with core account information.

    Stores essential user data including identifiers, profile details, and timestamps
    for account creation and updates."""

    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        profile_picture: Optional[bytes],
        bio: Optional[str],
        created_at: datetime,
        updated_at: Optional[datetime],
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.profile_picture = profile_picture
        self.bio = bio
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """Convert the AccountEntity instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the account data with serialized values
            for datetime and binary fields."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "profile_picture": base64.b64encode(self.profile_picture).decode("utf-8")
            if self.profile_picture
            else None,
            "bio": self.bio,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
