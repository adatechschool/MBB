# sessions\users\apps.py

"""Django app configuration for users app."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration class for the users application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        # Import signals to ensure they are registered
        import users.signals  # noqa
