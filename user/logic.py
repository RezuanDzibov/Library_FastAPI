from fastapi_users.authentication.jwt import JWTAuthentication
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from core.db import database
from user.models import User
from user.schemas import UserDB
from config import SECRET


users = User.__table__


auth_backend = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)


async def get_user_db():
    yield SQLAlchemyUserDatabase(UserDB, database, users)