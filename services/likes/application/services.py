from services.likes.domain.models import LikeModel
from services.posts.domain.models import PostModel  # Importation de PostModel
from services.likes.infrastructure.repositories import LikeRepository

class LikeService:
    def __init__(self, like_repository: LikeRepository):
        self.like_repository = like_repository

    def create_like(self, user, post_id):
        post = PostModel.objects.get(id=post_id)
        like = LikeModel(user=user, post=post)
        return self.like_repository.create(like)
    # Assuming PostModel is imported from the appropriate module
       

    def get_likes_by_user(self, user):
        return self.like_repository.get_by_user(user)

    def get_likes_by_post(self, post):
        return self.like_repository.get_by_post(post)

    def delete_like(self, user, post):
        return self.like_repository.delete(user, post) 