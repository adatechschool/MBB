# sessions\service\views.py

"""URL configuration for the sessions service."""

from django.urls import path

from sessions.service.interface_adapters.controllers import (
    SessionController,
    CookieTokenRefreshView,
)

urlpatterns = [
    path("add/", SessionController.as_view(), name="session_create"),
    path("current/", SessionController.as_view(), name="session_current"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
]
