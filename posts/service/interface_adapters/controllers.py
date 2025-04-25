# posts\service\interface_adapters\controllers.py

"""Controller for post-related HTTP requests and responses."""

from django.db.models import Count, Exists, OuterRef

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from common.response import success, error
from common.models import Post, Like
from posts.service.application.use_cases import PostUseCase
from posts.service.infrastructure.django_post_repository import DjangoPostRepository

_use_case = PostUseCase(DjangoPostRepository())


class PostListController(APIView):
    """GET /api/posts/ → list all posts."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            Post.objects.all()
            .annotate(
                likes_count=Count("like"),
                liked_by_user=Exists(
                    Like.objects.filter(post=OuterRef("pk"), user=request.user)
                ),
            )
            .order_by("-created_at")
        )

        payload = []
        for p in qs:
            payload.append({
                "post_id": p.post_id,
                "user_id": p.user_id,
                "post_content": p.post_content,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
                "likes_count": p.likes_count,
                "liked_by_user": p.liked_by_user,
            })

        return success(data=payload, http_status=status.HTTP_200_OK)


class PostCreateController(APIView):
    """POST /api/posts/create/ → create a new post."""

    def post(self, request):
        user_id = request.data.get("user_id")
        content = request.data.get("post_content")
        if not user_id or not content:
            return error(
                message="Both user_id and post_content are required.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        dto = _use_case.make_post(user_id, content)
        return success(
            data=dto.to_dict(),
            http_status=status.HTTP_201_CREATED,
        )
