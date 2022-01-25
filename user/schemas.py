import datetime
from uuid import UUID

from pydantic import BaseModel
from fastapi_users import models


class AdditionalUser(BaseModel):
    first_name: str
    last_name: str
    born_date: datetime.date
    current_avatar_id: UUID

    class Config:
        allow_mutation = True
        

class UserBook(BaseModel):
    id: UUID
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class User(AdditionalUser, models.BaseUser):
    pass


class UserCreate(AdditionalUser, models.BaseUserCreate):
    pass


class UserUpdate(AdditionalUser, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass