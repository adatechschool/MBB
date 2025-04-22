# common\models.py
# -*- coding: utf-8 -*-

"""Django models for a micro-blogging application.

This module contains the model definitions for the core entities of the micro-blogging
platform, including users, posts, comments, and follow relationships.
"""

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from common.managers import UserManager


class Role(models.Model):
    """Represents a user role within the platform."""

    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(
        max_length=255,
        choices=[("user", "User"), ("admin", "Admin"), ("moderator", "Moderator")],
        default="user",
    )

    class Meta:
        """Database table configuration for Role model."""

        db_table = "Role"
        verbose_name = "role"
        verbose_name_plural = "roles"


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for the micro-blogging application."""

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        help_text="Role assigned to this user",
    )
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        """Database table configuration for User model."""

        db_table = "User"
        verbose_name = "user"
        verbose_name_plural = "users"


class Session(models.Model):
    """Tracks active sessions for users."""

    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User associated with this session",
    )
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        """Database table configuration for Session model."""

        db_table = "Session"


class Post(models.Model):
    """Represents a user-created post."""

    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Author of the post",
    )
    post_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database table configuration for Post model."""

        db_table = "Post"


class Comment(models.Model):
    """User comments on posts."""

    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        help_text="Post this comment belongs to",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Author of the comment",
    )
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database table configuration for Comment model."""

        db_table = "Comment"


class Like(models.Model):
    """Likes by users on posts."""

    like_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        help_text="Post that was liked",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who liked the post",
    )

    class Meta:
        """Database table configuration for Like model with uniqueness constraint."""

        db_table = "Like"
        unique_together = (("post", "user"),)


class Hashtag(models.Model):
    """Hashtags associated with posts."""

    hashtag_id = models.AutoField(primary_key=True)
    hashtag_name = models.CharField(max_length=255, unique=True)

    class Meta:
        """Database table configuration for Hashtag model."""

        db_table = "Hashtag"


class PostHashtag(models.Model):
    """Join table linking posts and hashtags."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        help_text="Post tagged with the hashtag",
    )
    hashtag = models.ForeignKey(
        Hashtag,
        on_delete=models.CASCADE,
        help_text="Hashtag applied to the post",
    )

    class Meta:
        """Database table configuration for PostHashtag junction model with uniqueness constraint"""

        db_table = "Post_Hashtag"
        unique_together = (("post", "hashtag"),)


class Media(models.Model):
    """Media items attached to posts."""

    media_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        help_text="Post this media belongs to",
    )
    media_type = models.CharField(
        max_length=50,
        choices=[("image", "Image"), ("video", "Video")],
        default="image",
        blank=True,
    )
    media_content = models.BinaryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database table configuration for Media model."""

        db_table = "Media"


class Follow(models.Model):
    """Represents a follower/followee relationship between users."""

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        help_text="The user who follows",
    )
    followee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        help_text="The user being followed",
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Database table configuration for Follow model with uniqueness constraint."""

        db_table = "Follow"
        unique_together = (("follower", "followee"),)
