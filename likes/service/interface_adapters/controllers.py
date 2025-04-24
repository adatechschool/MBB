# likes\service\interface_adapters\controllers.py

"""Controller for user-related HTTP requests and responses."""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from common.response import success, error
from likes.service.application.use_cases import LikeUseCase
from likes.service.infrastructure.django_like_repository import DjangoLikeRepository


class LikesController(APIView):
    """Controller for listing all likes without authentication"""

    permission_classes = [AllowAny]
    use_case = LikeUseCase(DjangoLikeRepository())

    def post(self, request):
        """
        Retrieve all likes.
        """
        user_id = request.data.get("user_id")
        post_id = request.data.get("post_id")
        if not user_id or not post_id:
            return error(
                message="Both user_id and post_id are required.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        dtos = self.use_case.like_post(user_id, post_id)
        return success(
            data=[dto.to_dict() for dto in dtos],
            http_status=status.HTTP_200_OK,
        )
