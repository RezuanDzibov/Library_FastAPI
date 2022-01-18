from typing import AsyncGenerator

import databases
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from config import (
    SQL_ENGINE,
    SQL_USER,
    SQL_PASSWORD,
    SQL_HOST,
    SQL_PORT,
    SQL_DATABASE
)


SQLALCHEMY_DATABASE_URL = f'{SQL_ENGINE}://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}'
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
database = databases.Database(SQLALCHEMY_DATABASE_URL)
BaseModel: DeclarativeMeta = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session