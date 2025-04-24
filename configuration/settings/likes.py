# configuration\settings\likes.py

"""Django settings for the likes service."""

from configuration.settings.base import *  # noqa

# Service-specific apps
INSTALLED_APPS += [  # noqa
    "likes.service.apps.LikesServiceConfig",
]
