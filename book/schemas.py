import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    name: str
    price: int
    available: bool = True
    edition: str
    release_date: date

    class Config:
        allow_mutation = True
        orm_mode = True


class BookRetrieve(BookBase):
    id: uuid.UUID


class BookUpdate(BookBase):
    name: Optional[str]
    price: Optional[int]
    edition: Optional[str]
    available: Optional[bool]
    release_date: Optional[date]