# services\posts\domain\models.py

from django.db import models
from services.users.domain.models import UserModel


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
