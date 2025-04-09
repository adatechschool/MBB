# services/authentication/domain/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone


class AuthSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auth_sessions'
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Session for {self.user.username}"

    @property
    def is_valid(self):
        return timezone.now() < self.expires_at

    class Meta:
        # Explicitly set the app_label so Django associates this model with the auth app.
        app_label = 'authentication'
        db_table = "authentication_authsession"
