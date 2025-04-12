# services\follows\domain\models.py

from django.db import models
from services.users.domain.models import UserModel

class Follow(models.Model):
    follower = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
