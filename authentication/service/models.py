# authentication/service/models.py

"""Models for the authentication service, handling user sessions and tokens."""

from django.db import models
from django.conf import settings


class Session(models.Model):
    """Model for storing user authentication sessions with expiration."""

    session_id: models.AutoField = models.AutoField(primary_key=True)
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions"
    )
    token: models.CharField = models.CharField(max_length=255)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    expires_at: models.DateTimeField = models.DateTimeField()

    class Meta:
        """Metadata options for the Session model."""

        db_table = "Session"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Session {self.session_id} for {self.user}"


class Account(models.Model):
    """Model representing a user account with profile information and metadata."""

    user_id: models.AutoField = models.AutoField(primary_key=True)
    username: models.CharField = models.CharField(max_length=255)
    email: models.EmailField = models.EmailField(unique=True)
    profile_picture: models.BinaryField = models.BinaryField(null=True, blank=True)
    bio: models.TextField = models.TextField(null=True, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)
