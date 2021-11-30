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


def unauthorized_response(error_message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": error_message},
    )


def invalid_username_or_password_handler(
    request: Request, exc: InvalidUsernameOrPassword
) -> JSONResponse:
    return unauthorized_response("Username or password is invalid")


def user_already_exists_handler(
    request: Request, exc: UserAlreadyExists
) -> JSONResponse:
    return unauthorized_response(f"The username: {exc.username} is already in use")


def user_dont_exists_handler(request: Request, exc: UserDontExists) -> JSONResponse:
    return unauthorized_response(
        "An User could not be found to perform the required operation"
    )


def token_has_expired_handler(request: Request, exc: TokenHasExpired) -> JSONResponse:
    return unauthorized_response("The token has expired.")


def could_not_validate_handler(request: Request, exc: CouldNotValidate) -> JSONResponse:
    return unauthorized_response(f"It was not possible to validate token: {exc.detail}")
