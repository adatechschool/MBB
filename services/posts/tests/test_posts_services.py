# services/posts/tests/test_posts_services.py

import pytest
from datetime import datetime, timezone
from services.posts.application.services import PostService
from services.posts.domain.value_objects import PostDTO
from services.roles.domain.models import RoleModel
from django.contrib.auth import get_user_model

User = get_user_model()


class DummyPostRepository:
    def __init__(self):
        self.posts = []
        self.current_id = 1

    def create(self, post: PostDTO) -> PostDTO:
        new_post = PostDTO(
            id=self.current_id,
            title=post.title,
            content=post.content,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user=post.user,
        )
        self.posts.append(new_post)
        self.current_id += 1
        return new_post


@pytest.fixture
def dummy_repo():
    return DummyPostRepository()


@pytest.fixture
def post_service(dummy_repo):
    return PostService(dummy_repo)


@pytest.fixture
def test_user(db):
    default_role, _ = RoleModel.objects.get_or_create(role_name=RoleModel.USER)
    return User.objects.create_user(
        username="testuser",
        password="testpass",
        role=default_role  # supply the required role
    )


def test_create_post_success(post_service, test_user):
    title = "My First Post"
    content = "This is a test post."
    post = post_service.create_post(title, content, test_user)
    assert post.id > 0
    assert post.title == title
    assert post.content == content


def test_create_post_fail_empty_title(post_service, test_user):
    with pytest.raises(ValueError) as excinfo:
        post_service.create_post("", "Content", test_user)
    assert "Title cannot be empty" in str(excinfo.value)
