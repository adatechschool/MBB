from django.urls import path
from services.users.interface.views import UserView

urlpatterns = [
    path('user/', UserView.as_view(), name='user_view'),
    path('user/<int:id>/', UserView.as_view(), name='user_detail_view'),
    path('user/<int:id>/delete/', UserView.as_view(), name='user_delete_view'),
    path('user/<int:id>/update/', UserView.as_view(), name='user_update_view')
]
# This code defines URL patterns for user-related views in a Django application.
# It includes paths for viewing, creating, updating, and deleting users.
