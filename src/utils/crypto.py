import hashlib
import uuid
from typing import Optional


def get_salt_dot_hash(password: str, salt: Optional[str] = None):
    if salt is None:
        salt = uuid.uuid4().hex
    salted_password = (password + salt).encode()
    hashed_password = hashlib.sha512(salted_password).hexdigest()
    return f"{salt}.{hashed_password}"


def check_password(password, salt_dot_hash):
    hashed_password = get_salt_dot_hash(password, salt_dot_hash.split(".")[0])
    return salt_dot_hash == hashed_password
