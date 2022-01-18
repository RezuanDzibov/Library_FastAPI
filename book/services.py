from typing import Union
from uuid import UUID

from sqlalchemy import select, update, insert, delete
from sqlalchemy.exc import NoResultFound   # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, joinedload
from fastapi import HTTPException

from book.models import Book
from book.schemas import BookCreateIn, BookUpdate
from user.models import User
from utils import extract_objects, extract_object


async def get_books(session: AsyncSession, available: Union[bool, None], limit: int):
    statement = select(Book).options(   # type: ignore
        Load(Book).load_only(Book.id, Book.name, Book.price, Book.available),   # type: ignore
        joinedload(Book.user).load_only(User.first_name, User.last_name)
    )
    statement = statement.limit(limit)
    if available is not None:
        statement = statement.where(Book.available == available) #type: ignore
    books = await session.execute(statement)
    books = books.all()
    books = extract_objects(objects=books)
    return books


async def get_book(session: AsyncSession, book_id: UUID):
    statement = select(Book).options(   # type: ignore
        joinedload(Book.user).load_only(User.first_name, User.last_name)
    )
    statement = statement.where(Book.id == book_id)
    book = await session.execute(statement)
    book = book.one()
    book = extract_object(object=book)
    return book


async def insert_book(session: AsyncSession, item: BookCreateIn, user_id: UUID):
    book = item.dict()
    book['user_id'] = user_id.hex
    statement = insert(Book).values(book).returning('*')  # type: ignore 
    book = await session.execute(statement)
    await session.commit()
    book = book.one()
    return book


async def update_book(session: AsyncSession, book_id: UUID, item: BookUpdate):
    item = item.dict(exclude_unset=True)   # type: ignore
    statement = update(Book).where(Book.id == book_id).values(**item).returning('*')   # type: ignore
    book = await session.execute(statement)
    await session.commit()
    book = book.one()
    return book


async def delete_book(session: AsyncSession, book_id: UUID):
    try:
        statement = delete(Book).where(Book.id == book_id).returning('*')   # type: ignore
        book = await session.execute(statement)
        await session.commit()
        book = book.one()
        return book
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Book not found.')