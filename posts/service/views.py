# posts\service\views.py

"""URL configuration for the posts service."""

from django.urls import path
from posts.service.interface_adapters.controllers import (
    PostListController,
    PostCreateController,
)

urlpatterns = [
    path("list/", PostListController.as_view(), name="posts_list"),
    path("create/", PostCreateController.as_view(), name="posts_create"),
]

