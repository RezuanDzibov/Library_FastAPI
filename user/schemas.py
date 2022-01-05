import datetime

from pydantic import BaseModel
from fastapi_users import models


class AdditionalUser(BaseModel):
    first_name: str
    last_name: str
    born_date: datetime.date

    class Config:
        allow_mutation = True


class User(AdditionalUser, models.BaseUser):
    pass


class UserCreate(AdditionalUser, models.BaseUserCreate):
    pass


class UserUpdate(AdditionalUser, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass