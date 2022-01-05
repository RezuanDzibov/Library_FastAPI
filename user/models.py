from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, DATE, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.db import BaseModel
from core.models import UUIDMixin


class UserModel(BaseModel, SQLAlchemyBaseUserTable):
    __tablename__ = 'user'

    first_name = Column(String(255))
    last_name = Column(String(255))
    born_date = Column(DATE)
    author = relationship('AuthorModel', back_populates='user', uselist=False)
    publisher = relationship('PublisherModel', back_populates='user', uselist=False)


class AuthorModel(UUIDMixin, BaseModel):
    __tablename__ = 'author'

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('UserModel', back_populates='author')


class PublisherModel(UUIDMixin, BaseModel):
    __tablename__ = 'publisher'

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('UserModel', back_populates='publisher')