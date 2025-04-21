# sessions\service\domain\entities.py

"""Django ORM model for user sessions."""

from django.db import models


class SessionModel(models.Model):
    """Model representing user sessions with authentication tokens and expiry times."""

    session_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        """Database configuration for the Session model."""

        db_table = '"Session"'
        indexes = [models.Index(fields=["user_id"])]

        def __str__(self):
            return f"Session Meta for table {self.db_table}"

        def get_indexes(self):
            """Return the list of database indexes defined for this model."""
            return self.indexes
