from functools import lru_cache
from typing import Optional

import sqlmodel
from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.pool import StaticPool

from src.auth.user_model import StoredUser
from src.exceptions.exceptions import (InvalidUsernameOrPassword,
                                       UserAlreadyExists, UserDontExists)
from src.settings.settings import Settings, settings_factory
from src.user_repository.user_repository_interface import UserRepository


class StoredUserTable(StoredUser, sqlmodel.SQLModel, table=True):
    user_id: int = sqlmodel.Field(default=None, primary_key=True)
    username: str = sqlmodel.Field()
    salt_blank_hash: str = sqlmodel.Field()


class SQLUserRepository(UserRepository):
    """
    This class makes use of the SQLModel ORM (a wrapper to SQLAlchemy ORM).
    It works for almost any SQL database (see SQLAlchemy supported databases).
    To use a different database just set a new database connection string in the environment settings.
    """

    def __init__(self, settings: Settings) -> None:
        """Connects to SQL database"""
        if settings.DB_CONNECTION_STRING == "sqlite://":
            self.__engine = sqlmodel.create_engine(
                settings.DB_CONNECTION_STRING,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        else:
            self.__engine = sqlmodel.create_engine(settings.DB_CONNECTION_STRING)
        sqlmodel.SQLModel.metadata.create_all(self.__engine, checkfirst=True)

    def add_user(self, username: str, salt_blank_hash: str) -> None:
        with sqlmodel.Session(self.__engine) as session:
            user = StoredUserTable(username=username, salt_blank_hash=salt_blank_hash)
            stored_user = None
            try:
                stored_user = self.find(user.username)
            except InvalidUsernameOrPassword:
                pass
            if stored_user is not None:
                raise UserAlreadyExists(username=username)
            session.add(user)
            session.commit()
            session.refresh(user)

    def delete_user(self, user_id: int) -> None:
        with sqlmodel.Session(self.__engine) as session:
            try:
                statement = sqlmodel.select(StoredUserTable).where(
                    StoredUserTable.user_id == user_id
                )
                user = session.exec(statement).one()
                if user is not None:
                    session.delete(user)
                session.commit()
            except NoResultFound:
                raise UserDontExists()

    def update_user(
            self,
            user_id: int,
            email: Optional[str] = None,
            salt_blank_hash: Optional[str] = None,
    ) -> None:
        ...

    def find_by_id(self, user_id: int) -> StoredUser:
        ...

    def find(self, username: str) -> StoredUser:
        with sqlmodel.Session(self.__engine) as session:
            try:
                statement = sqlmodel.select(StoredUserTable).where(
                    StoredUserTable.username == username
                )
                user = session.exec(statement).one()
                return StoredUser(
                    username=user.username, salt_blank_hash=user.salt_blank_hash
                )
            except NoResultFound:
                raise InvalidUsernameOrPassword()


@lru_cache
def sql_user_repository_factory(
        settings: Settings = Depends(settings_factory),
) -> SQLUserRepository:
    return SQLUserRepository(settings)
