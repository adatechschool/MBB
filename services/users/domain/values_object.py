# services\users\domain\values_object.py

from dataclasses import dataclass
from datetime import datetime
from services.users.domain.models import UserModel

@dataclass(frozen=True)
class UserDTO:
    id: int
    username: str
    email: str
    role: UserModel
    created_at: datetime
    updated_at: datetime

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
