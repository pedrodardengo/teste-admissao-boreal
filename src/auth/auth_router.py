from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.auth.auth_service import AuthService, auth_service_factory
from src.auth.token_model import Token
from src.users.user_model import IncomingUser, StoredUser

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_user_from_token(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(auth_service_factory),
) -> StoredUser:
    """
    Every end point that wants to be protected by a OAuth2 standard needs to depend on this function.
    It will make sure a user can be retrieved from token
    :param token: A access_token
    :param auth_service: The authorization
    :return: a user
    """
    return auth_service.retrieve_user_from_token(token)


@router.post("/signup")
async def sign_up(
        user: IncomingUser, auth_service: AuthService = Depends(auth_service_factory)
) -> None:
    """
    Signs up the user in the repositories, it delegates to the
    auth service the task of interacting with the repositories.
    :param user: a User with username and password
    :param auth_service: An instance of an authorization service.
    :return: None
    """
    auth_service.save_user_in_repository(user)


@router.post("/token", response_model=Token)
async def get_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(auth_service_factory),
) -> Token:
    """
    Retrieves a token given that a form data containing an existing username with correct password.
    It will return a token object.
    :param form_data: form data from OAuth2
    :param auth_service: an authorization service
    :return: Token
    """
    user = IncomingUser(username=form_data.username, password=form_data.password)
    username = auth_service.authenticate_user(user)
    return auth_service.create_access_token(username)
