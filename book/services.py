from typing import Union
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from utils import extract_objects

from book.models import BookModel
from book.schemas import BookUpdate, BookBase



async def get_books(session: AsyncSession, available: Union[bool, None]):
    statement = select(BookModel)
    if available is not None:
        statement = statement.where(BookModel.available == available)
    books = await session.execute(statement)
    books = books.all()
    books = extract_objects(objects=books, many=True)
    return books


async def get_book(session: AsyncSession, book_id: UUID):
    statement = select(BookModel).where(BookModel.id == book_id)
    book = await session.execute(statement)
    book = book.one()
    book = extract_objects(objects=book, many=False)
    return book


async def insert_book(session: AsyncSession, item: BookBase):
    book = BookModel(**item.dict())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def update_book(session: AsyncSession, book_id: UUID, item: BookUpdate):
    item = item.dict(exclude_unset=True) # type: ignore
    statement = update(BookModel).where(BookModel.id == book_id).values(**item).returning('*') # type: ignore
    book = await session.execute(statement)
    await session.commit()
    book = book.one()
    return book


async def delete_book(session: AsyncSession, book_id: UUID):
    try:
        statement = select(BookModel).where(BookModel.id == book_id)
        book = await session.execute(statement)
        book = book.one()
        book = extract_objects(objects=book, many=False)
        await session.delete(book)
        await session.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Book not found.')