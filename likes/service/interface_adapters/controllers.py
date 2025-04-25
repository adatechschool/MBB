# likes\service\interface_adapters\controllers.py

"""Controller for user-related HTTP requests and responses."""

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from common.response import success, error
from likes.service.application.use_cases import LikeUseCase
from likes.service.infrastructure.django_like_repository import DjangoLikeRepository


class PostLikeController(APIView):
    permission_classes = [IsAuthenticated]
    use_case = LikeUseCase(DjangoLikeRepository())

    def post(self, request, post_id):
        try:
            dto = self.use_case.like_post(request.user.user_id, post_id)
            return success(data=dto.to_dict(), http_status=status.HTTP_200_OK)
        except Exception as e:
            return error(str(e), http_status=status.HTTP_400_BAD_REQUEST)


class PostUnlikeController(APIView):
    permission_classes = [IsAuthenticated]
    use_case = LikeUseCase(DjangoLikeRepository())

    def post(self, request, post_id):
        try:
            # call a new unlike method on the use case
            self.use_case.unlike_post(request.user.user_id, post_id)
            return success(data={}, http_status=status.HTTP_200_OK)
        except Exception as e:
            return error(str(e), http_status=status.HTTP_400_BAD_REQUEST)
