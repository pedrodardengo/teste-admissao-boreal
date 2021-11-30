from abc import ABC, abstractmethod
from typing import Optional

from src.auth.user_model import StoredUser


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, username: str, salt_blank_hash: str) -> None:
        """
        Adds a user to repository
        :param username: user's username
        :param salt_blank_hash: string with salt a blank space and a hash created using password + salt
        :return: None
        """
        ...

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """
        Deletes a user using as reference its id
        :param user_id: an integer
        :return: None
        """
        ...

    @abstractmethod
    def update_user(
            self,
            user_id: int,
            username: Optional[str] = None,
            salt_blank_hash: Optional[str] = None,
    ) -> None:
        """
        Updates an user using by reference its id;
        :param user_id: user's id
        :param username: user's username
        :param salt_blank_hash: string with salt a blank space and a hash created using password + salt
        :return: None
        """
        ...

    @abstractmethod
    def find(self, username: str) -> StoredUser:
        """
        Finds a user using its username as reference
        :param username: user's username
        :return: the found user
        """
        ...
