# services\posts\interfaces\views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.posts.application.services import PostService
from services.posts.infrastructure.repositories import PostRepository
from services.posts.infrastructure.serializers import PostSerializer

post_service = PostService(PostRepository())


class CreatePostView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                post = post_service.create_post(
                    title=serializer.validated_data['title'],
                    content=serializer.validated_data['content']
                )
                return Response({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'created_at': post.created_at
                }, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
