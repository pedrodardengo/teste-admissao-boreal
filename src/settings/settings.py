from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """These are the environment variables loaded using Pydantic's BaseSettings"""

    DB_CONNECTION_STRING: str


@lru_cache
def settings_factory() -> Settings:
    return Settings()
