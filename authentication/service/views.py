# authentication/service/views.py

"""URL configuration for authentication service endpoints."""

from django.urls import path

from authentication.service.interface_adapters.controllers import (
    RegisterController,
    LoginController,
    LogoutController,
)

urlpatterns = [
    path("login/", LoginController.as_view(), name="login"),
    path("register/", RegisterController.as_view(), name="register"),
    path("logout/", LogoutController.as_view(), name="logout"),
]
