# likes\service\views.py

"""URL configuration for user service endpoints."""

from django.urls import path

from likes.service.interface_adapters.controllers import LikesController

urlpatterns = [
    path("like/", LikesController.as_view(), name="like_post"),
]
