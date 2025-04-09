# services\posts\domain\models.py

from django.db import models
from dataclasses import dataclass
from datetime import datetime

class PostModel(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@dataclass(frozen=True)
class Post:
    id: int
    title: str
    content: str
    created_at: datetime

    def validate(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty.")
        if not self.content or not self.content.strip():
            raise ValueError("Content cannot be empty.")
