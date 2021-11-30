from functools import lru_cache
from typing import Optional

from src.auth.user_model import StoredUser
from src.exceptions.exceptions import (InvalidUsernameOrPassword,
                                       UserAlreadyExists)
from src.user_repository.user_repository_interface import UserRepository


class FakeUserRepository(UserRepository):

    def __init__(self):
        self.storage = []

    def find(self, username: str) -> StoredUser:
        for stored_user in self.storage:
            if stored_user.username == username:
                return stored_user
        raise InvalidUsernameOrPassword()

    def add_user(self, username: str, salt_blank_hash: str) -> None:
        for stored_user in self.storage:
            if stored_user.username == username:
                raise UserAlreadyExists(username=username)
        self.storage.append(StoredUser(username=username, salt_blank_hash=salt_blank_hash))

    def delete_user(self, user_id: int) -> None:
        ...

    def update_user(
            self,
            user_id: int,
            username: Optional[str] = None,
            salt_blank_hash: Optional[str] = None,
    ) -> None:
        ...


@lru_cache
def fake_user_repository_factory():
    return FakeUserRepository()
