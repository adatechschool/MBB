# users\service\views.py

"""URL configuration for user service endpoints."""

from django.urls import path

from users.service.interface_adapters.controllers import UsersController

urlpatterns = [
    path("get/users/", UsersController.as_view(), name="user_get"),
]
