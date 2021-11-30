from datetime import datetime, timedelta
from functools import lru_cache

import pytz
from pydantic import BaseModel


class FakeSettings(BaseModel):
    DB_CONNECTION_STRING: str = ''
    TOKEN_SECRET: str = 'token_secret'
    MINUTES_FOR_TOKEN_EXPIRATION: int = 60

    def get_expiration_date(self) -> datetime:
        now = datetime.now(pytz.timezone("America/Sao_Paulo"))
        return now + timedelta(minutes=self.MINUTES_FOR_TOKEN_EXPIRATION)

    def __hash__(self):
        return hash(self.DB_CONNECTION_STRING)


@lru_cache
def fake_settings_factory() -> FakeSettings:
    return FakeSettings()
