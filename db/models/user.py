import uuid

import sqlalchemy_utils as sau
from sqlalchemy import Column, String

from db.base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(sau.UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    email = Column(sau.EmailType)
    password = Column(sau.PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt']),
        unique=False,
        nullable=False
    )

