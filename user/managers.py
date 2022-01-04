from typing import Optional

from fastapi import Depends
from fastapi_users import BaseUserManager, models
from starlette.requests import Request

from user.logic import get_user_db
from user.schemas import UserCreate, UserDB
from config import SECRET


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: models.UD, request: Optional[Request] = None
    ) -> None:
        print(f'User {user.id} has registered')

    async def on_after_forgot_password(
        self, user: models.UD, token: str, request: Optional[Request] = None
    ) -> None:
        print(f'User {user.id} has forgot their password. Reset token {token}')

    async def on_after_request_verify(
        self, user: models.UD, token: str, request: Optional[Request] = None
    ) -> None:
        print(f'Verification requested for user {user.id}. Verification token {token}')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)