from datetime import datetime, timedelta
from functools import lru_cache

import pytz
from pydantic import BaseSettings


class Settings(BaseSettings):
    """These are the environment variables loaded using Pydantic's BaseSettings"""

    DB_CONNECTION_STRING: str
    TOKEN_SECRET: str
    MINUTES_FOR_TOKEN_EXPIRATION: int = 60

    def get_expiration_date(self) -> datetime:
        now = datetime.now(pytz.timezone("America/Sao_Paulo"))
        return now + timedelta(minutes=self.MINUTES_FOR_TOKEN_EXPIRATION)

    def __hash__(self):
        return hash(self.DB_CONNECTION_STRING)


@lru_cache
def settings_factory() -> Settings:
    return Settings()
