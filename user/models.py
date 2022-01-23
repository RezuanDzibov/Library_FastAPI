from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, DATE
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.db import BaseModel
from image.models import AvatarImage


class User(BaseModel, SQLAlchemyBaseUserTable): #type: ignore
    __tablename__ = 'user'

    first_name = Column(String(255))
    last_name = Column(String(255))
    born_date = Column(DATE)
    books = relationship('Book', back_populates='user')
    current_avatar_id = Column(UUID)
    avatars = relationship('AvatarImage', back_populates='user')