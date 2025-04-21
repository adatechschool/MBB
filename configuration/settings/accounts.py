# configuration\settings\accounts.py

"""Django settings for the accounts service."""

from configuration.settings.base import *  # noqa

# Service-specific apps
INSTALLED_APPS += [  # noqa
    "accounts.service.apps.AccountsServiceConfig",
]

# URLs & WSGI
ROOT_URLCONF = "accounts.config.urls"
WSGI_APPLICATION = "accounts.config.wsgi.application"
