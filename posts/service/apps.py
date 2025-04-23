# posts\service\apps.py

"""Django app configuration for the posts service."""

from django.apps import AppConfig


class PostsServiceConfig(AppConfig):
    """Configuration for the posts service Django app."""

    name = "posts.service"
    label = "posts_service"
