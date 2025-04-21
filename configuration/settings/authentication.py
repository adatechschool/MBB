# config/settings/authentication.py

"""Authentication service Django settings."""

from configuration.settings.base import (
    INSTALLED_APPS,
)

INSTALLED_APPS += [
    "authentication.service.apps.AuthenticationServiceConfig",
    "sessions.service.apps.SessionsServiceConfig",
    "users.service.apps.UsersServiceConfig",
]

ROOT_URLCONF = "authentication.config.urls"
WSGI_APPLICATION = "authentication.config.wsgi.application"
