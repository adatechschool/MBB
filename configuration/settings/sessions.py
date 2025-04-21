# config/settings/sessions.py

"""Django settings for the sessions service."""

from configuration.settings.base import (
    INSTALLED_APPS,
)

INSTALLED_APPS += [
    "sessions.service.apps.SessionsServiceConfig",
    "users.service.apps.UsersServiceConfig",
]

ROOT_URLCONF = "sessions.config.urls"
WSGI_APPLICATION = "sessions.config.wsgi.application"
