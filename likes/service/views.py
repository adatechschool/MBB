# likes\service\views.py

"""URL configuration for user service endpoints."""

from django.urls import path, include

from likes.service.interface_adapters.controllers import PostLikeController, PostUnlikeController

urlpatterns = [
    path("posts/<int:post_id>/like/", PostLikeController.as_view(), name="post-like"),
    path("posts/<int:post_id>/unlike/", PostUnlikeController.as_view(), name="post-unlike"),
]
