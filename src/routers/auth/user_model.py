import re

from pydantic import BaseModel, validator


class User(BaseModel):
    email: str
    password: str

    @validator("email")
    def email_must_be_valid(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, v):
            raise ValueError("Passed email is not valid")

    @validator("passoword")
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
