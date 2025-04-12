# services\roles\apps.py

from django.apps import AppConfig


class RolesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services.roles'
    label = 'roles'
