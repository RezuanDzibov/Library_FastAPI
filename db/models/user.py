import sqlalchemy_utils as sau
from sqlalchemy import Column, String

from db.base import BaseModel
from db.models.base import UUIDMixin


class User(UUIDMixin, BaseModel):
    __tablename__ = 'user'

    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    email = Column(sau.EmailType, unique=True)
    password = Column(sau.PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt']),
        unique=False,
        nullable=False
    )

