# services/authentication/tests/test_views.py

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_api(client):
    url = reverse('register')
    data = {
        "username": "apiuser",
        "password": "apipass",
        "email": "apiuser@example.com"
    }
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_login_api(client):
    # First, register a user
    reg_url = reverse('register')
    reg_data = {
        "username": "apiuser2",
        "password": "apipass2",
        "email": "apiuser2@example.com"
    }
    client.post(reg_url, reg_data, content_type="application/json")

    # Then login
    login_url = reverse('login')
    login_data = {
        "username": "apiuser2",
        "password": "apipass2"
    }
    response = client.post(login_url, login_data,
                           content_type="application/json")
    assert response.status_code == 200
    json_response = response.json()
    assert 'token' in json_response


@pytest.mark.django_db
def test_logout_api(client):
    # Register and login a user
    reg_url = reverse('register')
    reg_data = {
        "username": "apiuser3",
        "password": "apipass3",
        "email": "apiuser3@example.com"
    }
    client.post(reg_url, reg_data, content_type="application/json")

    login_url = reverse('login')
    login_data = {
        "username": "apiuser3",
        "password": "apipass3"
    }
    login_response = client.post(
        login_url, login_data, content_type="application/json")
    token = login_response.json().get("token")

    # Logout using the token in the Authorization header
    logout_url = reverse('logout')
    response = client.post(logout_url, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 200
