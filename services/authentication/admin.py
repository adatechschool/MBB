# services/authentication/admin.py

from django.contrib import admin
from services.authentication.domain.models import AuthSession

admin.site.register(AuthSession)
