from django.db import models
from django.contrib.auth.models import AbstractUser
from dataclasses import dataclass
from datetime import datetime

class Role(models.Model):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
    ]
    role_name = models.CharField(max_length=255, choices=ROLE_CHOICES, default=USER)
    
    def __str__(self):
        return self.role_name

class UserModel(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    bio = models.TextField(blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Correction pour éviter les conflits avec auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usermodel_set',  # Nom personnalisé pour éviter le conflit
        related_query_name='usermodel',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usermodel_set',  # Nom personnalisé pour éviter le conflit
        related_query_name='usermodel',
    )
    
    def __str__(self):
        return self.username

@dataclass
class User:
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    profile_image: str
    bio: str
    role_id: int
    created_at: datetime
    updated_at: datetime
    
    def __str__(self):
        return self.username