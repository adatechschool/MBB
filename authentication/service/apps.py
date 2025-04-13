# authentication\service\apps.py

"""Django app configuration for the authentication service."""

from django.apps import AppConfig


class ServiceConfig(AppConfig):
    """Django app configuration for the authentication service."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "service"
