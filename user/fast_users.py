from fastapi_users.fastapi_users import FastAPIUsers

from user.managers import get_user_manager
from user.logic import auth_backend
from user.schemas import UserCreate, UserUpdate, UserDB, User


fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
