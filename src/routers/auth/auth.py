from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.routers.auth.user_model import User
from src.user_repository.sql_user_repository import sql_user_repository_factory
from src.user_repository.user_repository_interface import UserRepository
from src.utils.crypto import get_salt_dot_hash

router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/users")
async def create_user(
    user: User, user_repo: UserRepository = Depends(sql_user_repository_factory)
) -> None:
    salt_dot_hash = get_salt_dot_hash(user.password)
    user_repo.add_user(user.email, salt_dot_hash)
