# services\likes\domain\models.py

from django.db import models
from services.posts.domain.models import UserModel, PostModel
from dataclasses import dataclass
from datetime import datetime


class LikeModel(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(
        PostModel, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

@dataclass
class Like:
    user: UserModel
    post: PostModel
    created_at: datetime
    
    def __init__(self):
        self.created_at = datetime.now()