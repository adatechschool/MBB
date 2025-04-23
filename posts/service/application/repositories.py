# posts\service\application\repositories.py

from abc import ABC, abstractmethod
from typing import List
from common.dtos import PostDTO


class PostRepositoryInterface(ABC):
    @abstractmethod
    def get_all_posts(self) -> List[PostDTO]:
        ...

    @abstractmethod
    def create_post(self, user_id: int, content: str) -> PostDTO:
        ...
