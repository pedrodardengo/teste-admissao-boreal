from fastapi import Depends, HTTPException
from jose import jwt
from starlette import status

from src.auth.token_model import Token
from src.auth.user_model import IncomingUser, StoredUser
from src.exceptions.invalid_username_or_password import InvalidUsernameOrPassword
from src.settings.settings import Settings, settings_factory
from src.user_repository.sql_user_repository import sql_user_repository_factory
from src.user_repository.user_repository_interface import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository, settings: Settings) -> None:
        self.__user_repo = user_repository
        self.__settings = settings

    def save_user_in_repository(self, user: IncomingUser) -> None:
        salt_dot_hash = user.get_salt_dot_hash()
        self.__user_repo.add_user(user.username, salt_dot_hash)

    def authenticate_user(self, user: IncomingUser) -> str:
        try:
            stored_user = self.__user_repo.find(user.username)
            is_valid = stored_user.is_password_valid(user.password)
            if not is_valid:
                raise InvalidUsernameOrPassword
            return user.username
        except InvalidUsernameOrPassword as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)

    def create_access_token(self, username: str) -> Token:
        data_to_encode = {"sub": username, "exp": self.__settings.get_expiration_date()}
        token = jwt.encode(data_to_encode, self.__settings.TOKEN_SECRET)
        return Token(access_token=token)

    def retrieve_user_from_token(self, token: str) -> StoredUser:
        try:
            data = jwt.decode(token, self.__settings.TOKEN_SECRET, algorithms=["HS256"])
            user = self.__user_repo.find(data.get("sub"))
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except InvalidUsernameOrPassword as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate token: {error}",
            )


def auth_service_factory(
    user_repository: UserRepository = Depends(sql_user_repository_factory),
    settings: Settings = Depends(settings_factory),
) -> AuthService:
    return AuthService(user_repository, settings)
