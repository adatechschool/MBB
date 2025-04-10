# services\users\interfaces\urls.py

from django.urls import path
from services.users.interfaces.views import UserDetailView

urlpatterns = [
    path('account/', UserDetailView.as_view(), name='user-detail'),
]
