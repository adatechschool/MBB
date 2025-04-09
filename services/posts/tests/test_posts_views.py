# services\posts\tests\test_views.py

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from services.posts.domain.models import RoleModel

User = get_user_model()


@pytest.mark.django_db
def test_create_post_api(client):
    default_role, _ = RoleModel.objects.get_or_create(role_name=RoleModel.USER)
    user = User.objects.create_user(
        username="api_post_user", password="testpass", role=default_role)
    client.force_login(user)
    url = reverse('create-post')  # Make sure this name matches your URLs
    data = {
        "title": "API Test Post",
        "content": "Content for the API test."
    }
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201
    json_response = response.json()
    assert json_response['title'] == data['title']


@pytest.mark.django_db
def test_list_posts_api(client):
    # Optionally, create some posts first via factory or directly
    url = reverse('list-posts')
    response = client.get(url)
    assert response.status_code == 200
    # Optionally assert the structure of your response
