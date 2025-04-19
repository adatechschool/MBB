# accounts/service/infrastructure/django_account_repository.py

"""Django ORM implementation of the account repository interface."""

import base64
from typing import Optional
from django.utils import timezone

from accounts.service.application.repositories import AccountRepositoryInterface
from accounts.service.core.entities import AccountEntity
from accounts.service.models import AccountModel


class DjangoAccountRepository(AccountRepositoryInterface):
    """Django ORM implementation of the account repository interface."""

    def get_account(self, user_id: int) -> Optional[AccountEntity]:
        try:
            user = AccountModel.objects.get(user_id=user_id)
        except AccountModel.DoesNotExist:
            return None
        picture_b64 = None
        if user.profile_picture:
            picture_b64 = base64.b64encode(user.profile_picture).decode()
        return AccountEntity(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            bio=user.bio,
            profile_picture=picture_b64,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def update_account(
        self,
        user_id: int,
        username: str,
        email: str,
        bio: str,
        profile_picture: Optional[str],
    ) -> AccountEntity:
        user = AccountModel.objects.get(user_id=user_id)
        user.username = username
        user.email = email
        user.bio = bio
        # decode incoming base64 if provided
        if profile_picture is not None:
            user.profile_picture = base64.b64decode(profile_picture)
        user.updated_at = timezone.now()
        user.save(
            update_fields=["username", "email", "bio", "profile_picture", "updated_at"]
        )
        return self.get_account(user_id)

    def delete_account(self, user_id: int) -> None:
        AccountModel.objects.filter(user_id=user_id).delete()
