from abc import ABC, abstractmethod
from typing import Any, Optional

from src.users.user_model import StoredUser


class UserRepository(ABC):

    @abstractmethod
    def add_user(self, username: str, salt_blank_hash: str) -> Optional[str]:
        """Adds a user to repositories"""
        ...

    @abstractmethod
    def delete_user(self, user_id: int) -> Optional[Any]:
        """Deletes a user using as reference its id"""
        ...

    @abstractmethod
    def update_user(
            self,
            user_id: int,
            username: Optional[str] = None,
            salt_blank_hash: Optional[str] = None,
    ) -> None:
        """Updates an user using by reference its id"""
        ...

    @abstractmethod
    def find(self, username: str) -> Optional[StoredUser]:
        """Finds a user using its username as reference"""
        ...
