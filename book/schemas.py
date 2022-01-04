from typing import Optional

from pydantic import BaseModel


class BookUpdate(BaseModel):
    name: Optional[str]
    price: Optional[int]
    edition: Optional[int]
    available: Optional[bool]

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    name: str
    price: int
    edition: int
    available: bool