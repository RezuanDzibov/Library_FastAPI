from sqlalchemy import Column, Integer, String, Boolean

from db.base import BaseModel
from db.models.base import UUIDMixin


class Book(UUIDMixin, BaseModel):
    __tablename__ = 'book'

    name = Column(String)
    price = Column(Integer)
    edition = Column(Integer)
    available = Column(Boolean, default=True)