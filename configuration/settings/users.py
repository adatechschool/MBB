# configuration\settings\users.py

"""Django settings for the users service."""

from configuration.settings.base import *  # noqa

# Service-specific apps
INSTALLED_APPS += [  # noqa
    "users.service.apps.UsersServiceConfig",
]
