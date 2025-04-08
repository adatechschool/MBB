# services\posts\interfaces\urls.py

from django.urls import path
from services.posts.interfaces.views import CreatePostView

urlpatterns = [
    path('posts/', CreatePostView.as_view(), name='create-post'),
]
