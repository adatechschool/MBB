# authentication/service/views.py

from django.urls import path
from service.interface_adapters.controllers.login_controller import LoginController
from service.interface_adapters.controllers.register_controller import RegisterController
from service.interface_adapters.controllers.logout_controller import LogoutController

urlpatterns = [
    path('login/', LoginController.as_view(), name='login'),
    path('register/', RegisterController.as_view(), name='register'),
    path('logout/', LogoutController.as_view(), name='logout'),
]
