from fastapi import FastAPI

from src.auth import auth_router
from src.breweries import brewerie_router
from src.exceptions.auth_handlers import (could_not_validate_handler,
                                          invalid_username_or_password_handler,
                                          token_has_expired_handler,
                                          user_already_exists_handler,
                                          user_dont_exists_handler)
from src.exceptions.exceptions import (CouldNotValidate,
                                       InvalidUsernameOrPassword,
                                       TokenHasExpired, UserAlreadyExists,
                                       UserDontExists)

app = FastAPI(title="Teste para Boreal", version="0.3.0")

app.add_exception_handler(
    InvalidUsernameOrPassword, invalid_username_or_password_handler
)
app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
app.add_exception_handler(UserDontExists, user_dont_exists_handler)
app.add_exception_handler(TokenHasExpired, token_has_expired_handler)
app.add_exception_handler(CouldNotValidate, could_not_validate_handler)

app.include_router(auth_router.router)
app.include_router(brewerie_router.router)
