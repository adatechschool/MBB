# authentication\users\models.py

"""Custom user model and manager for the authentication system."""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


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


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for authentication using email and username.

    Extends Django's AbstractBaseUser and PermissionsMixin to create a custom user
    model that uses email for authentication instead of username. Includes fields
    for email, username, active status, and staff status.
    """

    user_id: models.AutoField = models.AutoField(primary_key=True)
    email: models.EmailField = models.EmailField(unique=True)
    username: models.CharField = models.CharField(max_length=255, unique=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.email)
