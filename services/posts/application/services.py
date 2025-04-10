# services\posts\application\services.py

from datetime import datetime, timezone
from services.posts.domain.models import Post
from services.posts.infrastructure.repositories import PostRepository


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def create_post(self, title: str, content: str, user) -> Post:
        # Instantiate domain entity with all required fields
        now = datetime.now(timezone.utc)
        new_post = Post(
            id=0,
            title=title,
            content=content,
            created_at=now,
            updated_at=now,
            user=user,
        )
        new_post.validate()
        # Persist using the repository and return the stored post with an assigned ID
        return self.repository.create(new_post)

    def get_all_posts(self) -> list:
        return self.repository.get_all()
