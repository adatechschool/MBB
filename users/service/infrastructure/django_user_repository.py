# users\service\infrastructure\django_user_repository.py

"""Django ORM implementation of the user repository interface."""

import base64

from typing import List, Optional
from django.utils import timezone

from common.dtos import AccountDTO
from users.service.domain.entities import User
from users.service.application.repositories import UserRepositoryInterface


class DjangoUserRepository(UserRepositoryInterface):
    """Django ORM implementation of the user repository."""

    def get_all_users(self) -> List[AccountDTO]:
        users = User.objects.all()
        dtos: List[AccountDTO] = []
        for user in users:
            picture_b64: Optional[str] = None
            if user.profile_picture:
                try:
                    with user.profile_picture.open("rb") as img_file:
                        raw = img_file.read()
                    picture_b64 = base64.b64encode(raw).decode()
                except Exception:
                    picture_b64 = None
            dtos.append(
                AccountDTO(
                    user_id=user.user_id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                    date_joined=user.date_joined,
                    bio=user.bio,
                    profile_picture=picture_b64,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )
            )
        return dtos
