# services\likes\domain\value_objects.py

from dataclasses import dataclass
from datetime import datetime
from services.posts.domain.models import PostModel
from services.users.domain.models import UserModel

@dataclass
class LikeDTO:
    user: UserModel
    post: PostModel
    created_at: datetime

    def __init__(self):
        self.created_at = datetime.now()
