# configuration\settings\posts.py

"""Django settings for the posts service."""
from configuration.settings.base import *

# register the posts app
INSTALLED_APPS += [
    "posts.service.apps.PostsServiceConfig",
]

# override URLs & WSGI
ROOT_URLCONF = "posts.config.urls"
WSGI_APPLICATION = "posts.config.wsgi.application"
