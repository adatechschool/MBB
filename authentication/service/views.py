# authentication/service/views.py

from django.urls import path
from service.interface_adapters.controllers.auth_controller import AuthController

urlpatterns = [
    path('login/', AuthController.as_view(), name='login'),
]
