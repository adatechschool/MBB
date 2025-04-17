# accounts\service\views.py

"""URL configuration for account service endpoints."""

from django.urls import path
from service.interface_adapters.controllers.account_controller import AccountController

urlpatterns = [
    path("get/account/", AccountController.as_view(), name="account_get"),
    path("update/account/", AccountController.as_view(), name="account_update"),
    path("delete/account/", AccountController.as_view(), name="account_delete"),
]
