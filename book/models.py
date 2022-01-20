from datetime import datetime

from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Boolean, 
    DATE, 
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.db import BaseModel
from core.models import UUIDMixin
from image.models import BookImage


class Book(UUIDMixin, BaseModel): #type: ignore
    __tablename__ = 'book'

    name = Column(String)
    price = Column(Integer)
    edition = Column(String)
    available = Column(Boolean, default=True)
    release_date = Column(DATE)
    created = Column(DateTime, default=datetime.now) # TODO created_at
    updated = Column(DateTime, server_default=func.now()) # TODO on_update updated_at
    description = Column(String)
    language = Column(String)
    pages = Column(Integer)
    user_id = Column(UUID, ForeignKey('user.id'))
    user = relationship('User', back_populates='books')
    images = relationship('BookImage', back_populates='book')