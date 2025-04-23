# posts\service\application\use_cases.py

"""Use case layer for post operations."""

from typing import List
from posts.service.application.repositories import PostRepositoryInterface
from common.dtos import PostDTO


class PostUseCase:
    def __init__(self, repo: PostRepositoryInterface):
        self.repo = repo

    def list_posts(self) -> List[PostDTO]:
        return self.repo.get_all_posts()

    def make_post(self, user_id: int, content: str) -> PostDTO:
        return self.repo.create_post(user_id, content)
