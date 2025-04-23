# posts\service\interface_adapters\controllers.py

"""Controller for post-related HTTP requests and responses."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from posts.service.application.use_cases import PostUseCase
from posts.service.infrastructure.django_post_repository import DjangoPostRepository

_use_case = PostUseCase(DjangoPostRepository())


class PostListController(APIView):
    """GET /api/posts/ → list all posts."""

    def get(self, request):
        dtos = _use_case.list_posts()
        return Response(
            {"status": "success", "data": [dto.to_dict() for dto in dtos], "error": None},
            status=status.HTTP_200_OK,
        )


class PostCreateController(APIView):
    """POST /api/posts/create/ → create a new post."""

    def post(self, request):
        user_id = request.data.get("user_id")
        content = request.data.get("post_content")
        if not user_id or not content:
            return Response(
                {
                    "status": "error",
                    "data": None,
                    "error": {"message": "Both user_id and post_content are required."},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        dto = _use_case.make_post(user_id, content)
        return Response(
            {"status": "success", "data": dto.to_dict(), "error": None},
            status=status.HTTP_201_CREATED,
        )


