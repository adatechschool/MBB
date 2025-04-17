# sessions\service\views.py

"""URL configuration for the sessions service."""

from django.urls import path
from service.interface_adapters.controllers.session_controller import SessionController
from service.interface_adapters.controllers.session_controller import (
    CookieTokenRefreshView,
)

urlpatterns = [
    path("add/", SessionController.as_view(), name="session_create"),
    path("current/", SessionController.as_view(), name="session_create_or_current"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
]
