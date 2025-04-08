# services\posts\interfaces\urls.py

from django.urls import path
from services.posts.interfaces.views import CreatePostView, ListPostView

urlpatterns = [
    path('posts/', CreatePostView.as_view(), name='create-post'),
    path('posts/all/', ListPostView.as_view(), name='list-posts'),
]
