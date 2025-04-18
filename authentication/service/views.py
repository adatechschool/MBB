# authentication/service/views.py

"""URL configuration for the authentication service.

This module defines the URL patterns for the authentication endpoints including
login, logout and registration functionality.
"""

from django.urls import path
from authentication.service.interface_adapters.controllers.login_controller import (
    LoginController,
)
from authentication.service.interface_adapters.controllers.logout_controller import (
    LogoutController,
)
from authentication.service.interface_adapters.controllers.register_controller import (
    RegisterController,
)

urlpatterns = [
    path("login/", LoginController.as_view(), name="login"),
    path("register/", RegisterController.as_view(), name="register"),
    path("logout/", LogoutController.as_view(), name="logout"),
]
