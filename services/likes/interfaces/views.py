from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from services.likes.infrastructure.repositories import LikeRepository
from services.likes.application.services import LikeService
from services.likes.infrastructure.serializers import LikeSerializer

like_service = LikeService(LikeRepository())

class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        post = post_id  # Assuming post_id is the ID of the post being liked
        like = like_service.create_like(user, post)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        user = request.user
        post = post_id  # Assuming post_id is the ID of the post being unliked
        like_service.delete_like(user, post)
        return Response(status=status.HTTP_204_NO_CONTENT)