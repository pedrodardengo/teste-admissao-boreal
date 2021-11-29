import re
import uuid
from typing import Optional

from passlib.context import CryptContext
from pydantic import BaseModel, validator

crypto = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserIdentifier(BaseModel):
    username: str


class StoredUser(UserIdentifier):
    salt_dot_hash: str

    def is_password_valid(self, password: str) -> bool:
        salt, hashed_password = self.salt_dot_hash.split(".")
        return crypto.verify(password + salt, hashed_password)


class IncomingUser(UserIdentifier):
    password: str

    @validator("username")
    def username_must_be_an_email(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, v):
            raise ValueError("Passed email is not valid")

    @validator("password")
    def password_must_be_strong(cls, v):
        at_least_8_characters = len(v) > 8
        at_least_one_digit = re.search(r"\d", v) is not None
        at_least_one_uppercase = re.search(r"[A-Z]", v) is not None
        at_least_one_lowercase = re.search(r"[a-z]", v) is not None
        at_least_one_symbol = (
            re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', v) is not None
        )
        strong_password = all(
            [
                at_least_8_characters,
                at_least_one_digit,
                at_least_one_uppercase,
                at_least_one_lowercase,
                at_least_one_symbol,
            ]
        )
        if not strong_password:
            raise ValueError("Passed email is not valid")

    def get_salt_dot_hash(self, salt: Optional[str] = None):
        if salt is None:
            salt = uuid.uuid4().hex
        hashed_password = crypto.hash(self.password + salt)
        return f"{salt}.{hashed_password}"
