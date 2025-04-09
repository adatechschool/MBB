# services\posts\tests\test_views.py

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_post_api(client):
    url = reverse('create-post')
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
