# services/posts/infrastructure/repositories.py

from services.posts.domain.models import PostModel
from services.posts.domain.value_objects import PostDTO


class PostRepository:
    def create(self, post: PostDTO) -> PostDTO:
        post_model = PostModel.objects.create(
            title=post.title,
            content=post.content,
            user=post.user,  # Note: post.user must be provided
        )
        return PostDTO(
            id=post_model.id,
            title=post_model.title,
            content=post_model.content,
            created_at=post_model.created_at,
            updated_at=post_model.updated_at,
            user=post_model.user,
        )

    def get_all(self) -> list:
        posts = PostModel.objects.all()
        return [
            PostDTO(
                id=post.id,
                title=post.title,
                content=post.content,
                created_at=post.created_at,
                updated_at=post.updated_at,
                user=post.user,
            ) for post in posts
        ]
