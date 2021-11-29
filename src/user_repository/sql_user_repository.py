from functools import lru_cache
from typing import Optional

import sqlmodel
from sqlalchemy.exc import NoResultFound

from src.auth.user_model import StoredUser
from src.exceptions.invalid_username_or_password import InvalidUsernameOrPassword
from src.exceptions.user_already_exists import UserAlreadyExists
from src.exceptions.user_dont_exist import UserDontExists
from src.settings.settings import settings_factory
from src.user_repository.user_repository_interface import UserRepository


class StoredUserTable(StoredUser, sqlmodel.SQLModel, table=True):
    user_id: int = sqlmodel.Field(default=None, primary_key=True)
    username: str = sqlmodel.Field()
    salt_dot_hash: str = sqlmodel.Field()


class SQLUserRepository(UserRepository):
    """
    This class makes use of the SQLModel ORM (a wrapper to SQLAlchemy ORM).
    It works for almost any SQL database (see SQLAlchemy supported databases).
    To use a different database just set a new database connection string in the environment settings.
    """

    def __init__(self) -> None:
        """Connects to SQL database"""
        engine = sqlmodel.create_engine(settings_factory().DB_CONNECTION_STRING)
        sqlmodel.SQLModel.metadata.create_all(engine, checkfirst=True)
        self.session = sqlmodel.Session(engine)

    def add_user(self, username: str, salt_dot_hash: str) -> None:
        user = StoredUserTable(username=username, salt_dot_hash=salt_dot_hash)
        stored_user = None
        try:
            stored_user = self.find(user.username)
        except InvalidUsernameOrPassword:
            pass
        if stored_user is not None:
            raise UserAlreadyExists
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def delete_user(self, user_id: int) -> None:
        try:
            statement = sqlmodel.select(StoredUserTable).where(
                StoredUserTable.user_id == user_id
            )
            user = self.session.exec(statement).one()
            if user is not None:
                self.session.delete(user)
            self.session.commit()
        except NoResultFound:
            raise UserDontExists

    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        salt_dot_hash: Optional[str] = None,
    ) -> None:
        ...

    def find_by_id(self, user_id: int) -> StoredUser:
        ...

    def find(self, username: str) -> StoredUser:
        try:
            statement = sqlmodel.select(StoredUserTable).where(
                StoredUserTable.username == username
            )
            user = self.session.exec(statement).one()
            return StoredUser(username=user.username, salt_dot_hash=user.salt_dot_hash)
        except NoResultFound:
            raise InvalidUsernameOrPassword


@lru_cache
def sql_user_repository_factory() -> SQLUserRepository:
    return SQLUserRepository()
