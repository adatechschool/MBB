# services\posts\domain\value_objects.py

from dataclasses import dataclass
from datetime import datetime
from services.users.domain.models import UserModel

@dataclass(frozen=True)
class PostDTO:
    id: int
    title: str
    user: UserModel
    content: str
    created_at: datetime
    updated_at: datetime

    def validate(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty.")
        if not self.content or not self.content.strip():
            raise ValueError("Content cannot be empty.")
