# services\users\domain\models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class UserModel(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    bio = models.TextField(blank=True)
    role = models.ForeignKey(
        'roles.RoleModel', on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'users'
        swappable = 'AUTH_USER_MODEL'
