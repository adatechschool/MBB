# accounts/service/core/entities.py

"""Domain entity representing a user account."""

from datetime import datetime
from typing import Optional


class AccountEntity:
    """Domain entity representing a user account."""

    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        bio: Optional[str] = None,
        profile_picture: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.bio = bio
        self.profile_picture = profile_picture
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """Convert account entity to dictionary representation.

        Returns:
            dict: Dictionary containing account entity attributes.
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
