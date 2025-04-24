# likes\service\application\use_cases.py

from typing import List

from likes.service.application.repositories import LikeRepositoryInterface
from common.dtos import LikeDTO


class LikeUseCase:
    """Use case layer for like operations."""

    def __init__(self, repo: LikeRepositoryInterface):
        self.repo = repo

    def like_post(self, user_id: int, post_id: int) -> LikeDTO:
        """Like a post."""
        return self.repo.like_post(user_id, post_id)
