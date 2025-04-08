# services/posts/infrastructure/repositories.py

from services.posts.domain.models import Post
from django.db import models

# Optionally, define a Django model that corresponds to your domain entity


class PostModel(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


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
