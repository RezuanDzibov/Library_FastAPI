from sqlalchemy import Column, Integer, String, Boolean

from core.db import BaseModel
from core.models import UUIDMixin


class BookModel(UUIDMixin, BaseModel):
    __tablename__ = 'book'

    name = Column(String)
    price = Column(Integer)
    edition = Column(Integer)
    available = Column(Boolean, default=True)


books = BookModel.__table__