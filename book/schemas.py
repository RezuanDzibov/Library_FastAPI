from datetime import date
from typing import Optional, Union, List
from uuid import UUID

from pydantic import BaseModel, PositiveInt, constr
from typing_extensions import Literal

from user.schemas import UserBook
from image.schemas import ImageList


LanguageChoice = Union[
    Literal['en'],
    Literal['ru']
]

class BookBase(BaseModel):
    id: UUID
    name: str
    price: PositiveInt
    available: bool

    class Config:
        allow_mutation = True
        orm_mode = True


class BookList(BookBase):
    user: UserBook


class BookRetrieve(BookList):
    edition: str
    release_date: date
    description: str
    language: str
    pages: int
    user: UserBook
    images: List[ImageList]


class BookCreateIn(BaseModel):
    name: str
    price: PositiveInt
    edition: Optional[str] = ''
    available: bool = True
    release_date: date = date.today()
    description: str
    language: LanguageChoice  # type: ignore
    pages: PositiveInt
            
        
class BookCreateOut(BookBase):
    edition: str
    release_date: date
    description: str
    language: str
    pages: int    


class BookUpdate(BaseModel):
    name: Optional[str]
    price: Optional[PositiveInt]
    edition: Optional[str]
    available: Optional[bool]
    release_date: Optional[date]
    description: Optional[str]
    language: Optional[constr(min_length=2, max_length=2)] # type: ignore
    pages: Optional[PositiveInt]