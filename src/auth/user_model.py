import re
import uuid
from typing import Optional

from passlib.context import CryptContext
from pydantic import BaseModel, validator

crypto = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserIdentifier(BaseModel):
    username: str


class StoredUser(UserIdentifier):
    salt_blank_hash: str

    def is_password_valid(self, password: str) -> bool:
        salt, hashed_password = self.salt_blank_hash.split(" ")
        return crypto.verify(password + salt, hashed_password)


class IncomingUser(UserIdentifier):
    password: str

    @validator("username")
    def username_must_be_an_email(cls, username):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not bool(re.fullmatch(regex, username)):
            raise ValueError("Passed email is not valid")
        return username

    @validator("password")
    def password_must_be_strong(cls, password):
        has_8_characters = len(password) >= 8
        has_at_least_one_digit = re.search(r"\d", password) is not None
        has_at_least_one_uppercase = re.search(r"[A-Z]", password) is not None
        has_at_least_one_lowercase = re.search(r"[a-z]", password) is not None
        has_at_least_one_symbol = (
                re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is not None
        )
        strong_password = all(
            [
                has_8_characters,
                has_at_least_one_digit,
                has_at_least_one_uppercase,
                has_at_least_one_lowercase,
                has_at_least_one_symbol,
            ]
        )
        if not strong_password:
            raise ValueError(
                "Password must contain a minimum of 8 characters, at least "
                "one digit, one uppercase, one lowercase and one symbol"
            )
        return password

    def get_salt_blank_hash(self, salt: Optional[str] = None):
        if salt is None:
            salt = uuid.uuid4().hex
        hashed_password = crypto.hash(self.password + salt)
        return f"{salt} {hashed_password}"
