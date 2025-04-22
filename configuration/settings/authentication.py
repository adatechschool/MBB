# config/settings/authentication.py

"""Authentication service Django settings."""

from configuration.settings.base import *  # noqa

INSTALLED_APPS += [  # noqa
    "authentication.service.apps.AuthenticationServiceConfig",
    "sessions.service.apps.SessionsServiceConfig",
]

ROOT_URLCONF = "authentication.config.urls"
WSGI_APPLICATION = "authentication.config.wsgi.application"
