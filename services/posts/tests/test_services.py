# services\posts\tests\test_services.py

import pytest
from datetime import datetime, timezone
from services.posts.application.services import PostService
from services.posts.domain.models import Post


class DummyPostRepository:
    """A dummy repository to simulate persistence in tests."""

    def __init__(self):
        self.posts = []
        self.current_id = 1

    def create(self, post: Post) -> Post:
        new_post = Post(
            id=self.current_id,
            title=post.title,
            content=post.content,
            created_at=datetime.now(timezone.utc)
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


def test_create_post_success(post_service):
    title = "My First Post"
    content = "This is a test post."
    post = post_service.create_post(title, content)
    assert post.id > 0
    assert post.title == title
    assert post.content == content


def test_create_post_fail_empty_title(post_service):
    with pytest.raises(ValueError) as excinfo:
        post_service.create_post("", "Content")
    assert "Title cannot be empty" in str(excinfo.value)
