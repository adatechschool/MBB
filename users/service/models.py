# users\service\models.py

"""Models for the users service."""

from django.contrib.auth.models import (
    BaseUserManager,
)
from django.db import models  # noqa


class CustomUserManager(BaseUserManager):
    """Custom user manager for handling user creation and superuser creation."""

    def create_user(self, email, username, password=None, **extra_fields):
        """Create and save a new user instance.

        Args:
            email: User's email address
            username: User's username
            password: User's password (optional)
            **extra_fields: Additional fields to be saved

        Returns:
            User: The created user instance

        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and save a new superuser instance.

        Args:
            email: User's email address
            username: User's username
            password: User's password (optional)
            **extra_fields: Additional fields to be saved

        Returns:
            User: The created superuser instance
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)
