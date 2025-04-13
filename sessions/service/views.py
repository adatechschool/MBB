# sessions\service\views.py

"""URL configuration for the sessions service."""

from django.urls import path
from service.interface_adapters.controllers.session_controller import SessionController

urlpatterns = [
    path("current/", SessionController.as_view(), name="session_create_or_current"),
    path("<int:session_id>/", SessionController.as_view(), name="session_detail"),
]
