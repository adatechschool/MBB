# authentication/service/models.py

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
