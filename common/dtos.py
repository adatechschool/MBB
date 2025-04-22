# common\dtos.py

"""Data Transfer Objects (DTOs) for the micro-blogging application.

This module contains Pydantic models used for data validation and serialization
across different services in the application."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AccountDTO(BaseModel):
    """Data transfer object representing a user account in the micro-blogging system.

    Contains core user information, account status, join date, optional profile details,
    and timestamps. Inherits from Pydantic BaseModel for validation and serialization.
    """

    user_id: int
    username: str
    email: str
    is_active: bool
    date_joined: datetime
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    def update_profile(
        self,
        bio: Optional[str] = None,
        profile_picture: Optional[str] = None,
    ) -> None:
        """Update the user's profile information in the DTO.

        Args:
            bio: New biography text
            profile_picture: New profile picture URL
        """
        if bio is not None:
            self.bio = bio
        if profile_picture is not None:
            self.profile_picture = profile_picture

    def to_dict(self) -> dict:
        """Convert the DTO to a standard dictionary."""
        return self.model_dump()


class AuthDTO(BaseModel):
    """Data transfer object for authentication tokens."""

    access: str
    refresh: str

    def to_dict(self) -> dict:
        """Convert the DTO to a standard dictionary."""
        return self.model_dump()


class SessionDTO(BaseModel):
    """Data transfer object for user sessions."""

    session_id: int
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime

    def to_dict(self) -> dict:
        """Convert the DTO to a standard dictionary."""
        return self.model_dump()
