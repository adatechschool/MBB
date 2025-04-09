# services/posts/infrastructure/repositories.py

from services.posts.domain.models import Post
from django.db import models
from services.users.domain.models import UserModel # Assuming UserModel is defined in the same module as PostModel
    
class PostModel(models.Model):
        title = models.CharField(max_length=255)
        user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        # Nice to do
        # liked_by = models.ManyToManyField(User, through='Like', related_name='liked_posts')
        # hashtags = models.ManyToManyField('Hashtag', through='PostHashtag', related_name='posts')
        class Meta:
            db_table = '"Post"'

        def __str__(self):
            return f"Post {self.id} by {self.user.username}"


class PostRepository:
    def create(self, post: Post) -> Post:
        post_model = PostModel.objects.create(
            title=post.title,
            user=post.user,
            content=post.content,
        )
        return Post(
            id=post_model.id,
            title=post_model.title,
            content=post_model.content,
            created_at=post_model.created_at,
            updated_at=post_model.updated_at
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
