from functools import lru_cache
from typing import Optional

import sqlmodel
from sqlalchemy.exc import NoResultFound

from src.settings.settings import settings_factory
from src.user_repository.user_repository_interface import UserRepository


class StoredUser(sqlmodel.SQLModel, table=True):
    user_id: int = sqlmodel.Field(default=None, primary_key=True)
    email: str = sqlmodel.Field()
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

    def add_user(self, email: str, salt_dot_hash: str) -> None:
        user = StoredUser(email=email, salt_dot_hash=salt_dot_hash)
        # try:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        # except IntegrityError as e:
        #    ...
        # raise Exception

    def delete_user(self, user_id: int) -> None:
        try:
            statement = sqlmodel.select(StoredUser).where(StoredUser.user_id == user_id)
            invalid_cpf = self.session.exec(statement).one()
            if invalid_cpf is not None:
                self.session.delete(invalid_cpf)
            self.session.commit()
        except NoResultFound:
            pass

    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        salt_dot_hash: Optional[str] = None,
    ) -> None:
        ...

    def find_one(self, user_id: int) -> StoredUser:
        ...

    def find(self, email: str) -> list[StoredUser]:
        ...


@lru_cache
def sql_user_repository_factory() -> SQLUserRepository:
    return SQLUserRepository()
