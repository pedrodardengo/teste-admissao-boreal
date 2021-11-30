from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.exceptions.exceptions import (
    CouldNotValidate,
    InvalidUsernameOrPassword,
    TokenHasExpired,
    UserAlreadyExists,
    UserDontExists,
)


def invalid_username_or_password_handler(
    request: Request, exc: InvalidUsernameOrPassword
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "Username or password is invalid"},
    )


def user_already_exists_handler(
    request: Request, exc: UserAlreadyExists
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": f"The username: {exc.username} is already in use"},
    )


def user_dont_exists_handler(request: Request, exc: UserDontExists) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "An User could not be found to perform the required operation"
        },
    )


def token_has_expired_handler(request: Request, exc: TokenHasExpired) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "The token has expired."},
    )


def could_not_validate_handler(request: Request, exc: CouldNotValidate) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "It was not possible to validate token"},
    )
