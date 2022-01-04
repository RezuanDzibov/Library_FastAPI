from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase

from core.db import database
from user.models import UserModel
from user.schemas import UserDB
from config import SECRET


users = UserModel.__table__


auth_backends = [
    JWTAuthentication(secret=SECRET, lifetime_seconds=3600),
]


async def get_user_db():
    yield SQLAlchemyUserDatabase(UserDB, database, users)