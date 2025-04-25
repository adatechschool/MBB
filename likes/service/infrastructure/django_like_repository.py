# likes\service\infrastructure\django_like_repository.py

from typing import List
from django.utils import timezone
from common.models import Like
from common.dtos import LikeDTO
from likes.service.application.repositories import LikeRepositoryInterface


class DjangoLikeRepository(LikeRepositoryInterface):
    def create_like(self, user_id: int, post_id: int) -> LikeDTO:
        l = Like.objects.create(user_id=user_id, post_id=post_id)
        return LikeDTO(post_id=l.post_id, user_id=l.user_id)

    def delete_like(self, user_id: int, post_id: int) -> None:
        Like.objects.filter(user_id=user_id, post_id=post_id).delete()
