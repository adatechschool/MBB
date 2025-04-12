# services\users\tests\test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from services.roles.domain.models import RoleModel

User = get_user_model()


@pytest.fixture
def test_user(db):
    default_role, _ = RoleModel.objects.get_or_create(role_name=RoleModel.USER)
    user = User.objects.create_user(
        username='testuser', password='testpass', email='test@example.com', role=default_role)
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_get_user_details(client, test_user):
    client.force_authenticate(user=test_user)
    url = reverse('user-detail')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == test_user.username


@pytest.mark.django_db
def test_update_user_account(client, test_user):
    client.force_authenticate(user=test_user)
    url = reverse('user-detail')
    update_data = {'bio': 'Updated bio',
                   'first_name': 'John', 'last_name': 'Doe'}
    response = client.patch(url, update_data, format='json')
    assert response.status_code == 200
    data = response.json()
    assert data['bio'] == 'Updated bio'
    assert data['first_name'] == 'John'
    assert data['last_name'] == 'Doe'


@pytest.mark.django_db
def test_delete_user_account(client, test_user):
    client.force_authenticate(user=test_user)
    url = reverse('user-detail')
    response = client.delete(url)
    assert response.status_code == 200
    with pytest.raises(User.DoesNotExist):
        User.objects.get(id=test_user.id)


