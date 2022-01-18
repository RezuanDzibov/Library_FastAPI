from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, DATE
from sqlalchemy.orm import relationship

from core.db import BaseModel


class User(BaseModel, SQLAlchemyBaseUserTable): #type: ignore
    __tablename__ = 'user'

    first_name = Column(String(255))
    last_name = Column(String(255))
    born_date = Column(DATE)
    books = relationship('Book', back_populates='user')