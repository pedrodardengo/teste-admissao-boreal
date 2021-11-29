from abc import ABC, abstractmethod
from typing import Optional


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, email: str, salt_dot_hash: str) -> None:
        ...

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        ...

    @abstractmethod
    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        salt_dot_hash: Optional[str] = None,
    ) -> None:
        ...

    @abstractmethod
    def find_one(self, user_id: int):
        ...

    @abstractmethod
    def find(self, email: str):
        ...
