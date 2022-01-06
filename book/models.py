from sqlalchemy import Column, Integer, String, Boolean, DATE

from core.db import BaseModel
from core.models import UUIDMixin


class BookModel(UUIDMixin, BaseModel):
    __tablename__ = 'book'

    name = Column(String)
    price = Column(Integer)
    edition = Column(String)
    available = Column(Boolean, default=True)
    release_date = Column(DATE)