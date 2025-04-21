# accounts\service\domain\entities.py

"""Django ORM model for user accounts."""

from django.db import models


class AccountModel(models.Model):
    """Model representing a user account in the system."""

    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    role_id = models.IntegerField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    profile_picture = models.BinaryField(null=True, blank=True)
    bio = models.TextField(blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Model representing a user account in the system."""

        db_table = '"User"'
