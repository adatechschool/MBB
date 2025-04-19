# config/settings/accounts.py

"""Django settings for the accounts service."""

from config.settings.base import (
    INSTALLED_APPS,
)

# Service-specific apps
INSTALLED_APPS += [
    "accounts.service.apps.AccountsServiceConfig",
    "users.service.apps.UsersServiceConfig",
]

# URLs & WSGI
ROOT_URLCONF = "accounts.config.urls"
WSGI_APPLICATION = "accounts.config.wsgi.application"
