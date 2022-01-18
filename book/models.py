from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Boolean, 
    DATE, 
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from core.db import BaseModel
from core.models import UUIDMixin


class Book(UUIDMixin, BaseModel): #type: ignore
    __tablename__ = 'book'

    name = Column(String)
    price = Column(Integer)
    edition = Column(String)
    available = Column(Boolean, default=True)
    release_date = Column(DATE)
    description = Column(String)
    language = Column(String)
    pages = Column(Integer)
    user_id = Column(UUID, ForeignKey('user.id'))
    user = relationship('User', back_populates='books')