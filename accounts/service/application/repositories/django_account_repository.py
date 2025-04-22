# accounts\service\application\repositories\django_account_repository.py

"""Django implementation of the account repository interface."""

from typing import Optional
from service.application.repositories.account_repository import (
    AccountRepositoryInterface,
)
from service.core.entities.account import AccountEntity
from service.models import Account


class DjangoAccountRepository(AccountRepositoryInterface):
    """Django implementation of the Account repository for database operations."""

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
        profile_picture: Optional[bytes],
    ) -> AccountEntity:
        acc = Account.objects.get(user_id=user_id)
        acc.username = username
        acc.email = email
        acc.bio = bio
        if profile_picture is not None:
            acc.profile_picture = profile_picture
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
