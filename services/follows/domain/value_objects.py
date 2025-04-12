# services\follows\domain\value_objects.py

from dataclasses import dataclass
from datetime import datetime
from services.users.domain.models import UserModel

@dataclass(frozen=True)
class FollowDTO:
    follower: UserModel
    following: UserModel
    created_at: datetime

    def __init__(self):
        self.created_at = datetime.now()
