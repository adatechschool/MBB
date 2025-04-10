# services\posts\domain\models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from dataclasses import dataclass
from datetime import datetime


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
        app_label = 'posts'  # Explicitly set the app label


class UserModel(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    bio = models.TextField(blank=True)
    role = models.ForeignKey(
        RoleModel, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'posts'
        swappable = 'AUTH_USER_MODEL'


def get_default_user():
    from services.posts.domain.models import UserModel
    user, _ = UserModel.objects.get_or_create(username='default')
    return user.pk


class PostModel(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'posts'


@dataclass(frozen=True)
class Post:
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user: UserModel

    def validate(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty.")
        if not self.content or not self.content.strip():
            raise ValueError("Content cannot be empty.")
