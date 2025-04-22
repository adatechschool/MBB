# micro_blogging.py

"""SQLAlchemy models for a micro-blogging application.

This module defines the database models and relationships for a micro-blogging
platform using SQLAlchemy ORM.
"""

import datetime
from typing import List, Optional

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKeyConstraint,
    Integer,
    LargeBinary,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DEFAULT_TIMESTAMP_SERVER = "'2025-04-12 21:13:09.965294+02'::timestamp with time zone"
USER_ID_REF = "User.user_id"
POST_ID_REF = "Post.post_id"


class Base(DeclarativeBase):
    """Base class for all database models."""

    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Hashtag(Base):
    """Model representing hashtags used in posts."""

    __tablename__ = "Hashtag"
    __table_args__ = (PrimaryKeyConstraint("hashtag_id", name="Hashtag_pkey"),)

    hashtag_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hashtag_name: Mapped[str] = mapped_column(String(255))

    post: Mapped[List["Post"]] = relationship(
        "Post", secondary="Post_Hashtag", back_populates="hashtag"
    )


class Role(Base):
    """Model representing user roles in the system."""

    __tablename__ = "Role"
    __table_args__ = (
        CheckConstraint(
            "role_name::text = ANY (ARRAY['user'::character varying, "
            "'admin'::character varying, 'moderator'::character varying]::text[])",
            name="Role_role_name_check",
        ),
        PrimaryKeyConstraint("role_id", name="Role_pkey"),
    )

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(
        String(255), server_default=text("'user'::character varying")
    )

    User: Mapped[List["User"]] = relationship("User", back_populates="role")


class User(Base):
    """Model representing users in the system with their roles and profile information."""

    __tablename__ = "User"
    __table_args__ = (
        ForeignKeyConstraint(
            ["role_id"], ["Role.role_id"], name="user_role_id_foreign"
        ),
        PrimaryKeyConstraint("user_id", name="User_pkey"),
        UniqueConstraint("email", name="user_email_unique"),
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(True, 0),
        server_default=text(DEFAULT_TIMESTAMP_SERVER),
    )
    profile_picture: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))

    role: Mapped["Role"] = relationship("Role", back_populates="User")
    Post: Mapped[List["Post"]] = relationship("Post", back_populates="user")
    Session: Mapped[List["Session"]] = relationship("Session", back_populates="user")
    Comment: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")
    Like: Mapped[List["Like"]] = relationship("Like", back_populates="user")


t_Follow = Table(
    "Follow",
    Base.metadata,
    Column("follower_id", Integer, nullable=False),
    Column("followee_id", Integer, nullable=False),
    Column(
        "followed_at",
        TIMESTAMP(True, 0),
        nullable=False,
        server_default=text(DEFAULT_TIMESTAMP_SERVER),
    ),
    ForeignKeyConstraint(
        ["followee_id"], [USER_ID_REF], name="follow_followee_id_foreign"
    ),
    ForeignKeyConstraint(
        ["follower_id"], [USER_ID_REF], name="follow_follower_id_foreign"
    ),
)


class Post(Base):
    """Represents a post in the micro-blogging system with its content and metadata."""

    def __init__(self, user_id: int, post_content: str):
        """Initialize a new post.

        Args:
            user_id: The ID of the user creating the post
            post_content: The content of the post
        """
        super().__init__()
        self.user_id = user_id
        self.post_content = post_content

    __tablename__ = "Post"
    __table_args__ = (
        ForeignKeyConstraint(["user_id"], [USER_ID_REF], name="post_user_id_foreign"),
        PrimaryKeyConstraint("post_id", name="Post_pkey"),
    )

    post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    post_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(True, 0),
        server_default=text(DEFAULT_TIMESTAMP_SERVER),
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))

    hashtag: Mapped[List["Hashtag"]] = relationship(
        "Hashtag", secondary="Post_Hashtag", back_populates="post"
    )
    user: Mapped["User"] = relationship("User", back_populates="Post")
    Comment: Mapped[List["Comment"]] = relationship("Comment", back_populates="post")
    Like: Mapped[List["Like"]] = relationship("Like", back_populates="post")
    Media: Mapped[List["Media"]] = relationship("Media", back_populates="post")


class Session(Base):
    """Session model representing user authentication sessions.

    Attributes:
        session_id: Unique identifier for the session
        user_id: Foreign key reference to the User table
        token: Authentication token string
        created_at: Timestamp when session was created
        expires_at: Timestamp when session expires
    """

    __tablename__ = "Session"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"], [USER_ID_REF], name="session_user_id_foreign"
        ),
        PrimaryKeyConstraint("session_id", name="Session_pkey"),
    )

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    token: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(True, 0),
        server_default=text(DEFAULT_TIMESTAMP_SERVER),
    )
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(True, 0))

    user: Mapped["User"] = relationship("User", back_populates="Session")


class Comment(Base):
    """Represents a comment made by a user on a post.

    Attributes:
        comment_id: Unique identifier for the comment
        post_id: ID of the post this comment belongs to
        user_id: ID of the user who made the comment
        comment_content: The text content of the comment
        created_at: Timestamp when comment was created
        updated_at: Timestamp when comment was last updated
    """

    __tablename__ = "Comment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["post_id"], [POST_ID_REF], name="comment_post_id_foreign"
        ),
        ForeignKeyConstraint(
            ["user_id"], [USER_ID_REF], name="comment_user_id_foreign"
        ),
        PrimaryKeyConstraint("comment_id", name="Comment_pkey"),
    )

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    comment_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(True, 0),
        server_default=text(DEFAULT_TIMESTAMP_SERVER),
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))

    post: Mapped["Post"] = relationship("Post", back_populates="Comment")
    user: Mapped["User"] = relationship("User", back_populates="Comment")


class Like(Base):
    """Represents a like on a post in the micro-blogging system."""

    __tablename__ = "Like"
    __table_args__ = (
        ForeignKeyConstraint(["post_id"], [POST_ID_REF], name="like_post_id_foreign"),
        ForeignKeyConstraint(["user_id"], [USER_ID_REF], name="like_user_id_foreign"),
        PrimaryKeyConstraint("like_id", name="Like_pkey"),
    )

    like_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)

    post: Mapped["Post"] = relationship("Post", back_populates="Like")
    user: Mapped["User"] = relationship("User", back_populates="Like")


class Media(Base):
    """Represents a media attachment (image or video) for a post in the micro-blogging system."""

    __tablename__ = "Media"
    __table_args__ = (
        CheckConstraint(
            "media_type::text = ANY (ARRAY['image'::character varying,"
            " 'video'::character varying]::text[])",
            name="Media_media_type_check",
        ),
        ForeignKeyConstraint(["post_id"], [POST_ID_REF], name="media_post_id_foreign"),
        PrimaryKeyConstraint("media_id", name="Media_pkey"),
    )

    media_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(True, 0),
        server_default=text(DEFAULT_TIMESTAMP_SERVER),
    )
    media_type: Mapped[Optional[str]] = mapped_column(
        String(255), server_default=text("'image'::character varying")
    )
    media_content: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))

    post: Mapped["Post"] = relationship("Post", back_populates="Media")


t_Post_Hashtag = Table(
    "Post_Hashtag",
    Base.metadata,
    Column("post_id", Integer),
    Column("hashtag_id", Integer),
    ForeignKeyConstraint(
        ["hashtag_id"], ["Hashtag.hashtag_id"], name="post_hashtag_hashtag_id_foreign"
    ),
    ForeignKeyConstraint(
        ["post_id"], [POST_ID_REF], name="post_hashtag_post_id_foreign"
    ),
)
