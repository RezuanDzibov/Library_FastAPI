from datetime import datetime

from sqlalchemy import (
    Column, 
    String, 
    Boolean, 
    DateTime, 
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.db import BaseModel
from core.models import UUIDMixin


class ImageMixin:
    title = Column(String(length=255))
    available = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.now)
    image_path = Column(String)



class BookImage(UUIDMixin, ImageMixin, BaseModel):   # type: ignore
    __tablename__ = 'book_image'
    
    book_id = Column(UUID, ForeignKey('book.id'))
    book = relationship('Book', back_populates='images')