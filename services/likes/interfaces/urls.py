from django.urls import path
from services.likes.interfaces.views import LikeView

urlpatterns = [
    path('posts/<int:post_id>/like/', LikeView.as_view(), name='like_post'),
    path('posts/<int:post_id>/unlike/', LikeView.as_view(), name='unlike_post'),
]