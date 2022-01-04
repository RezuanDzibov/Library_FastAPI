from fastapi_users import FastAPIUsers

from user.managers import get_user_manager
from user.logic import auth_backends
from user.schemas import UserCreate, UserUpdate, UserDB, User


fastapi_users = FastAPIUsers(
    get_user_manager,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
