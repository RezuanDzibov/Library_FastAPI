import uuid

from sqlalchemy import Column, Integer, String, Boolean
import sqlalchemy_utils as sau

from db.base import BaseModel


class Book(BaseModel):
    __tablename__ = 'book'

    id = Column(sau.UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    price = Column(Integer)
    edition = Column(Integer)
    available = Column(Boolean, default=True)