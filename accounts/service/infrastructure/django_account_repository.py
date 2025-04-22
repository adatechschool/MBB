# accounts\service\infrastructure\django_account_repository.py

"""Django ORM implementation of the account repository interface."""

import base64
import uuid
from typing import Optional
from django.utils import timezone
from django.core.files.base import ContentFile
from django.db import IntegrityError

from accounts.service.application.repositories import AccountRepositoryInterface
from accounts.service.domain.entities import User
from accounts.service.exceptions import AccountNotFound, AccountConflict
from common.dtos import AccountDTO

ACCOUNT_NOT_FOUND_MESSAGE = "Account not found."
ALREADY_EXISTS_MESSAGE = "Username or email already taken."


class DjangoAccountRepository(AccountRepositoryInterface):
    """Django ORM implementation of the account repository interface."""

    def get_account(self, user_id: int) -> Optional[AccountDTO]:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist as exc:
            raise AccountNotFound(ACCOUNT_NOT_FOUND_MESSAGE) from exc
        picture_b64 = None
        if user.profile_picture:
            try:
                with user.profile_picture.open("rb") as img_file:
                    raw_bytes = img_file.read()
                picture_b64 = base64.b64encode(raw_bytes).decode()
            except Exception as exc:  # noqa
                picture_b64 = None
        return AccountDTO(
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

    def update_account(
        self,
        user_id: int,
        username: str,
        email: str,
        bio: str,
        profile_picture: Optional[str],
    ) -> AccountDTO:
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist as exc:
            raise AccountNotFound(ACCOUNT_NOT_FOUND_MESSAGE) from exc

        if User.objects.exclude(user_id=user_id).filter(email=email).exists():
            raise AccountConflict(ALREADY_EXISTS_MESSAGE)

        if User.objects.exclude(user_id=user_id).filter(username=username).exists():
            raise AccountConflict(ALREADY_EXISTS_MESSAGE)

        user.username = username or user.username
        user.email = email or user.email
        user.bio = bio or user.bio
        if profile_picture is not None:
            decoded_bytes = base64.b64decode(profile_picture)
            file_name = f"avatar_{user_id}_{uuid.uuid4().hex}.png"
            user.profile_picture.save(
                file_name,
                ContentFile(decoded_bytes),
                save=False,
            )
        user.updated_at = timezone.now()
        try:
            user.save(
                update_fields=[
                    "username",
                    "email",
                    "bio",
                    "profile_picture",
                    "updated_at",
                ]
            )
        except IntegrityError as exc:
            raise AccountConflict(ALREADY_EXISTS_MESSAGE) from exc
        return self.get_account(user_id)

    def delete_account(self, user_id: int) -> None:
        deleted_count, _ = User.objects.filter(user_id=user_id).delete()
        if deleted_count == 0:
            raise AccountNotFound(ACCOUNT_NOT_FOUND_MESSAGE)
