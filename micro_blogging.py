from typing import List, Optional

from sqlalchemy import CheckConstraint, Column, ForeignKeyConstraint, Integer, LargeBinary, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Hashtag(Base):
    __tablename__ = 'Hashtag'
    __table_args__ = (
        PrimaryKeyConstraint('hashtag_id', name='Hashtag_pkey'),
    )

    hashtag_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hashtag_name: Mapped[str] = mapped_column(String(255))

    post: Mapped[List['Post']] = relationship('Post', secondary='Post_Hashtag', back_populates='hashtag')


class Role(Base):
    __tablename__ = 'Role'
    __table_args__ = (
        CheckConstraint("role_name::text = ANY (ARRAY['user'::character varying, 'admin'::character varying, 'moderator'::character varying]::text[])", name='Role_role_name_check'),
        PrimaryKeyConstraint('role_id', name='Role_pkey')
    )

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String(255), server_default=text("'user'::character varying"))

    User: Mapped[List['User']] = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'User'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['Role.role_id'], name='user_role_id_foreign'),
        PrimaryKeyConstraint('user_id', name='User_pkey'),
        UniqueConstraint('email', name='user_email_unique')
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(True, 0), server_default=text("'2025-04-12 21:13:09.965294+02'::timestamp with time zone"))
    profile_picture: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))

    role: Mapped['Role'] = relationship('Role', back_populates='User')
    Post: Mapped[List['Post']] = relationship('Post', back_populates='user')
    Session: Mapped[List['Session']] = relationship('Session', back_populates='user')
    Comment: Mapped[List['Comment']] = relationship('Comment', back_populates='user')
    Like: Mapped[List['Like']] = relationship('Like', back_populates='user')


t_Follow = Table(
    'Follow', Base.metadata,
    Column('follower_id', Integer, nullable=False),
    Column('followee_id', Integer, nullable=False),
    Column('followed_at', TIMESTAMP(True, 0), nullable=False, server_default=text("'2025-04-12 21:13:09.965294+02'::timestamp with time zone")),
    ForeignKeyConstraint(['followee_id'], ['User.user_id'], name='follow_followee_id_foreign'),
    ForeignKeyConstraint(['follower_id'], ['User.user_id'], name='follow_follower_id_foreign')
)


class Post(Base):
    __tablename__ = 'Post'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='post_user_id_foreign'),
        PrimaryKeyConstraint('post_id', name='Post_pkey')
    )

    post_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    post_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(True, 0), server_default=text("'2025-04-12 21:13:09.965294+02'::timestamp with time zone"))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))

    hashtag: Mapped[List['Hashtag']] = relationship('Hashtag', secondary='Post_Hashtag', back_populates='post')
    user: Mapped['User'] = relationship('User', back_populates='Post')
    Comment: Mapped[List['Comment']] = relationship('Comment', back_populates='post')
    Like: Mapped[List['Like']] = relationship('Like', back_populates='post')
    Media: Mapped[List['Media']] = relationship('Media', back_populates='post')


class Session(Base):
    __tablename__ = 'Session'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='session_user_id_foreign'),
        PrimaryKeyConstraint('session_id', name='Session_pkey')
    )

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    token: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(True, 0), server_default=text("'2025-04-12 21:13:09.965294+02'::timestamp with time zone"))
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(True, 0))

    user: Mapped['User'] = relationship('User', back_populates='Session')


class Comment(Base):
    __tablename__ = 'Comment'
    __table_args__ = (
        ForeignKeyConstraint(['post_id'], ['Post.post_id'], name='comment_post_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='comment_user_id_foreign'),
        PrimaryKeyConstraint('comment_id', name='Comment_pkey')
    )

    comment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    comment_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(True, 0), server_default=text("'2025-04-12 21:13:09.965294+02'::timestamp with time zone"))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))

    post: Mapped['Post'] = relationship('Post', back_populates='Comment')
    user: Mapped['User'] = relationship('User', back_populates='Comment')


class Like(Base):
    __tablename__ = 'Like'
    __table_args__ = (
        ForeignKeyConstraint(['post_id'], ['Post.post_id'], name='like_post_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='like_user_id_foreign'),
        PrimaryKeyConstraint('like_id', name='Like_pkey')
    )

    like_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)

    post: Mapped['Post'] = relationship('Post', back_populates='Like')
    user: Mapped['User'] = relationship('User', back_populates='Like')


class Media(Base):
    __tablename__ = 'Media'
    __table_args__ = (
        CheckConstraint("media_type::text = ANY (ARRAY['image'::character varying, 'video'::character varying]::text[])", name='Media_media_type_check'),
        ForeignKeyConstraint(['post_id'], ['Post.post_id'], name='media_post_id_foreign'),
        PrimaryKeyConstraint('media_id', name='Media_pkey')
    )

    media_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(True, 0), server_default=text("'2025-04-12 21:13:09.965294+02'::timestamp with time zone"))
    media_type: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("'image'::character varying"))
    media_content: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))

    post: Mapped['Post'] = relationship('Post', back_populates='Media')


t_Post_Hashtag = Table(
    'Post_Hashtag', Base.metadata,
    Column('post_id', Integer),
    Column('hashtag_id', Integer),
    ForeignKeyConstraint(['hashtag_id'], ['Hashtag.hashtag_id'], name='post_hashtag_hashtag_id_foreign'),
    ForeignKeyConstraint(['post_id'], ['Post.post_id'], name='post_hashtag_post_id_foreign')
)
