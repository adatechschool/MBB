# likes\service\application\use_cases.py

from typing import List

from likes.service.application.repositories import LikeRepositoryInterface
from common.dtos import LikeDTO


class LikeUseCase:
    def __init__(self, repo: LikeRepositoryInterface):
        self.repo = repo

    def like_post(self, user_id: int, post_id: int) -> LikeDTO:
        return self.repo.create_like(user_id, post_id)

    def unlike_post(self, user_id: int, post_id: int) -> None:
        self.repo.delete_like(user_id, post_id)
