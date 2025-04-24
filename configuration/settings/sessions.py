# configuration\settings\sessions.py

"""Django settings for the sessions service."""

from configuration.settings.base import *  # noqa

INSTALLED_APPS += [  # noqa
    "sessions.service.apps.SessionsServiceConfig",
]

ROOT_URLCONF = "sessions.config.urls"
WSGI_APPLICATION = "sessions.config.wsgi.application"
