# likes\service\application\repositories.py

from abc import ABC, abstractmethod
from typing import List
from common.dtos import LikeDTO


class LikeRepositoryInterface(ABC):
    @abstractmethod
    def create_like(self, user_id: int, post_id: int) -> LikeDTO:
        ...
