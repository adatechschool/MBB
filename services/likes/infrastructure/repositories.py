from services.likes.domain.models import LikeModel
from services.likes.domain.value_objects import LikeDTO

class LikeRepository:
    def create(self, like: LikeDTO) -> LikeModel:
        like_model = LikeModel(
            user=like.user,
            post=like.post
        )
        like_model.save()
        return like_model

    def get_by_user(self, user) -> list[LikeModel]:
        return LikeModel.objects.filter(user=user)

    def get_by_post(self, post) -> list[LikeModel]:
        return LikeModel.objects.filter(post=post)

    def delete(self, user, post) -> bool:
        try:
            like = LikeModel.objects.get(user=user, post=post)
            like.delete()
            return True
        except LikeModel.DoesNotExist:
            return False