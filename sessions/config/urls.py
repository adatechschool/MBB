# sessions\config\urls.py

"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include  # noqa
from service.interface_adapters.controllers.refresh_token_controller import (
    RefreshTokenController,
)
from service.interface_adapters.controllers.session_controller import SessionController

urlpatterns = [
    path("api/sessions/add/", SessionController.as_view(), name="session_create"),
    path(
        "api/sessions/current/",
        SessionController.as_view(),
        name="session_create_or_current",
    ),
    path(
        "api/sessions/refresh/", RefreshTokenController.as_view(), name="token_refresh"
    ),
    path(
        "api/sessions/<int:session_id>/",
        SessionController.as_view(),
        name="session_detail",
    ),
]
