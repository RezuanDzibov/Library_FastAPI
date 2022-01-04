import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from config import (
    SQL_ENGINE,
    SQL_USER,
    SQL_PASSWORD,
    SQL_HOST,
    SQL_PORT,
    SQL_DATABASE
)


SQLALCHEMY_DATABASE_URL = f'{SQL_ENGINE}://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}'


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
database = databases.Database(SQLALCHEMY_DATABASE_URL)
BaseModel: DeclarativeMeta = declarative_base()