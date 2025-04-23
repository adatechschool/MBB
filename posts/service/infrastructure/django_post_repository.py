# posts\service\infrastructure\django_post_repository.py

from typing import List
from django.utils import timezone
from common.models import Post
from common.dtos import PostDTO
from posts.service.application.repositories import PostRepositoryInterface


class DjangoPostRepository(PostRepositoryInterface):
    def get_all_posts(self) -> List[PostDTO]:
        posts = Post.objects.select_related('user').all().order_by('-created_at')
        dtos = [
            PostDTO(
                post_id=p.post_id,
                user_id=p.user.user_id,
                post_content=p.post_content,
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
            for p in posts
        ]
        return dtos

    def create_post(self, user_id: int, content: str) -> PostDTO:
        p = Post.objects.create(
            user_id=user_id,
            post_content=content,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        return PostDTO(
            post_id=p.post_id,
            user_id=p.user_id,
            post_content=p.post_content,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
