# services\roles\domain\models.py

from django.db import models

class RoleModel(models.Model):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
    ]

    role_name = models.CharField(
        max_length=255, choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return self.role_name

    class Meta:
        app_label = 'roles'
