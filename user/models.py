from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, DATE

from core.db import BaseModel


class UserModel(BaseModel, SQLAlchemyBaseUserTable):
    __tablename__ = 'user'

    first_name = Column(String(255))
    last_name = Column(String(255))
    born_date = Column(DATE)
