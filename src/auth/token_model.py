from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DecodedTokenData(BaseModel):
    username: str
    exp: str

    def has_token_expired(self) -> bool:
        ...
