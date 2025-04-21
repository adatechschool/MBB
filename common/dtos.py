# common\dtos.py

"""Data Transfer Objects (DTOs) for the micro-blogging application.

This module contains Pydantic models used for data validation and serialization
across different services in the application.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AccountDTO(BaseModel):
    """Data transfer object representing a user account in the micro-blogging system.

    Contains core user information like ID, username, email and optional profile details.
    Inherits from Pydantic BaseModel for data validation and serialization.
    """

    user_id: int
    username: str
    email: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    def update_profile(
        self, bio: Optional[str] = None, profile_picture: Optional[str] = None
    ) -> None:
        """Update the user's profile information.

        Args:
            bio: Optional new biography text
            profile_picture: Optional new profile picture (base64 encoded)
        """
        if bio is not None:
            self.bio = bio
        if profile_picture is not None:
            self.profile_picture = profile_picture

    def to_dict(self) -> dict:
        """Convert the DTO to a dictionary representation.

        Returns:
            Dict containing the DTO's fields and values
        """
        return self.dict()


class AuthDTO(BaseModel):
    """Data transfer object for authentication tokens.

    Attributes:
            access: Access token string
            refresh: Refresh token string
    """

    access: str
    refresh: str

    def to_dict(self) -> dict:
        """Convert the DTO to a dictionary representation.

        Returns:
            Dict containing the DTO's fields and values
        """
        return self.dict()


class SessionDTO(BaseModel):
    """Data transfer object for user sessions.

    Attributes:
        session_id: Unique identifier for the session
        user_id: ID of the user this session belongs to
        token: Session authentication token
        created_at: Timestamp when session was created
        expires_at: Timestamp when session expires
    """

    session_id: int
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime

    def to_dict(self) -> dict:
        """Convert the DTO to a dictionary representation.

        Returns:
            Dict containing the DTO's fields and values
        """
        return self.dict()
