# accounts/service/infrastructure/django_account_repository.py

import base64
from typing import Optional
from accounts.service.application.repositories import AccountRepositoryInterface
from accounts.service.core.entities import AccountEntity
from accounts.service.models import Account


class DjangoAccountRepository(AccountRepositoryInterface):
    """Django ORM implementation of AccountRepositoryInterface"""

    def get_account(self, user_id: int) -> Optional[AccountEntity]:
        try:
            acc = Account.objects.get(user_id=user_id)
            return AccountEntity(
                user_id=acc.user_id,
                username=acc.username,
                email=acc.email,
                profile_picture=acc.profile_picture,
                bio=acc.bio,
                created_at=acc.created_at,
                updated_at=acc.updated_at,
            )
        except Account.DoesNotExist:
            return None

    def update_account(
        self,
        user_id: int,
        username: str,
        email: str,
        bio: str,
        profile_picture: Optional[str],
    ) -> AccountEntity:
        acc = Account.objects.get(user_id=user_id)
        acc.username = username
        acc.email = email
        acc.bio = bio
        if profile_picture is not None:
            # support base64 data URLs or raw string
            if profile_picture.startswith("data:"):
                _, encoded = profile_picture.split(",", 1)
                decoded = base64.b64decode(encoded)
            else:
                decoded = profile_picture.encode("utf-8")
            acc.profile_picture = decoded
        acc.save()
        return AccountEntity(
            user_id=acc.user_id,
            username=acc.username,
            email=acc.email,
            profile_picture=acc.profile_picture,
            bio=acc.bio,
            created_at=acc.created_at,
            updated_at=acc.updated_at,
        )

    def delete_account(self, user_id: int) -> None:
        Account.objects.filter(user_id=user_id).delete()
