from fastapi import Depends
from jose import jwt

from src.auth.token_model import Token
from src.auth.user_model import IncomingUser, StoredUser
from src.exceptions.exceptions import (CouldNotValidate,
                                       InvalidUsernameOrPassword,
                                       TokenHasExpired)
from src.settings.settings import Settings, settings_factory
from src.user_repository.sql_user_repository import sql_user_repository_factory
from src.user_repository.user_repository_interface import UserRepository


class AuthService:
    """Implements the actual logic of the authorization process"""

    def __init__(self, user_repository: UserRepository, settings: Settings) -> None:
        """
        :param user_repository: Any implementation of a UserRepository
        :param settings: Any implementation of a Settings
        """
        self.__user_repo = user_repository
        self.__settings = settings

    def save_user_in_repository(self, user: IncomingUser) -> None:
        """
        Saves a user in a implementation of the UsersRepository. The password is not saved directly but a string
        with a salt a blank space and the has of the password + salt is used in its place.
        :param user: a user with username and password
        :return: None
        """
        salt_blank_hash = user.get_salt_blank_hash()
        self.__user_repo.add_user(user.username, salt_blank_hash)

    def authenticate_user(self, user: IncomingUser) -> str:
        """
        Finds a user using its username than verifies if the passwords are the same.
        :param user: a user with username and password.
        :return: the verified user's username
        """
        stored_user = self.__user_repo.find(user.username)
        is_valid = stored_user.is_password_valid(user.password)
        if not is_valid:
            raise InvalidUsernameOrPassword()
        return user.username

    def create_access_token(self, username: str) -> Token:
        """
        Creates an access token with a given expiration date set in the settings and a given username.
        :param username: a username
        :return: A Token instance.
        """
        data_to_encode = {"sub": username, "exp": self.__settings.get_expiration_date()}
        token = jwt.encode(data_to_encode, self.__settings.TOKEN_SECRET)
        return Token(access_token=token)

    def retrieve_user_from_token(self, token: str) -> StoredUser:
        """
        Decodes the Token, and returns the user that was encoded.
        :param token: A Token object
        :return: a user with username and salt_blank_hash
        """
        try:
            data = jwt.decode(token, self.__settings.TOKEN_SECRET, algorithms=["HS256"])
            user = self.__user_repo.find(data.get("sub"))
            return user
        except jwt.ExpiredSignatureError:
            raise TokenHasExpired()
        except Exception:
            raise CouldNotValidate()


def auth_service_factory(
        user_repository: UserRepository = Depends(sql_user_repository_factory),
        settings: Settings = Depends(settings_factory),
) -> AuthService:
    return AuthService(user_repository, settings)
