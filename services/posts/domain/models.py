# services\posts\domain\models.py

from django.db import models
from dataclasses import dataclass
from datetime import datetime


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
