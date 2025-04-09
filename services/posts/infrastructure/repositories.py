# services/posts/infrastructure/repositories.py

from services.posts.domain.models import Post, PostModel


class PostRepository:
    def create(self, post: Post) -> Post:
        post_model = PostModel.objects.create(
            title=post.title,
            content=post.content,
        )
        return Post(
            id=post_model.id,
            title=post_model.title,
            content=post_model.content,
            created_at=post_model.created_at
        )

    def get_all(self) -> list:
        posts = PostModel.objects.all()
        return [
            Post(
                id=post.id,
                title=post.title,
                content=post.content,
                created_at=post.created_at
            ) for post in posts
        ]
