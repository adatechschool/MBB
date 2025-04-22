# authentication\service\apps.py

"""Django app configuration for the authentication service."""

from django.apps import AppConfig


class AuthenticationServiceConfig(AppConfig):
    """Configuration class for the authentication service."""

    name = "authentication.service"
    label = "authentication_service"
