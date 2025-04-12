# services\likes\domain\models.py

from django.db import models
from services.posts.domain.models import PostModel
from services.users.domain.models import UserModel


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
