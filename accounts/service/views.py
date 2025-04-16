# accounts\service\views.py

"""URL configuration for account service endpoints."""

from django.urls import path
from service.interface_adapters.controllers.account_controller import AccountController

urlpatterns = [
    path("me/", AccountController.as_view(), name="account_me"),
    path("me/update/", AccountController.as_view(), name="account_me_update"),
    path("get/<int:user_id>/", AccountController.as_view(), name="account_detail"),
    path("update/<int:user_id>/", AccountController.as_view(), name="account_update"),
    path("delete/<int:user_id>/", AccountController.as_view(), name="account_delete"),
]
