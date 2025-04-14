# accounts\service\views.py

"""Account model for managing user account data in the microblogging application."""

from django.db import models


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
