from typing import Union
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, update, insert, delete
from sqlalchemy.exc import NoResultFound   # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load, joinedload, subqueryload
from fastapi_pagination.ext.async_sqlalchemy import paginate

from book.models import Book
from book.schemas import BookCreateIn, BookUpdate
from user.models import User
from image.models import BookImage
from core.utils import extract_object


async def get_books(session: AsyncSession, available: Union[bool, None]):
    statement = select(Book).options(   # type: ignore
        Load(Book).load_only(Book.id, Book.name, Book.price, Book.available),   # type: ignore
        joinedload(Book.user).load_only(User.first_name, User.last_name)
    )
    if available is not None:
        statement = statement.where(Book.available == available) #type: ignore
    books = await paginate(session=session, query=statement)
    return books


async def get_book(session: AsyncSession, book_id: UUID):
    statement = select(Book).options(   # type: ignore
        joinedload(Book.user).load_only(User.first_name, User.last_name),
        subqueryload(Book.images.and_(BookImage.available == True)).load_only(BookImage.id, BookImage.title)
    )
    statement = statement.where(Book.id == book_id)
    result = await session.execute(statement)
    try: 
        book = result.one()
        book = extract_object(object=book)
        return book
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no book with this ID: {book_id}')
        

async def insert_book(session: AsyncSession, item: BookCreateIn, user_id: UUID):
    book = item.dict()
    book['user_id'] = user_id.hex
    statement = insert(Book).values(book).returning('*')  # type: ignore 
    result = await session.execute(statement)
    await session.commit()
    book = result.one()
    return book


async def update_book(session: AsyncSession, book_id: UUID, item: BookUpdate, user_id: UUID):
    item = item.dict(exclude_unset=True)   # type: ignore
    statement = update(Book).where(Book.id == book_id, Book.user_id == user_id.hex).values(**item).returning('*')   # type: ignore
    try: 
        result = await session.execute(statement)
        await session.commit()
        book = result.one()
        return book
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no book with this ID: {book_id} which belongs you')


async def delete_book(session: AsyncSession, book_id: UUID, user_id: UUID):
    statement = delete(Book).where(Book.id == book_id, Book.user_id == user_id.hex).returning('*')   # type: ignore
    try:
        result = await session.execute(statement)
        await session.commit()
        book = result.one()
        return book
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no book with this ID: {book_id} which belongs you')
    

async def get_book_user_id(session: AsyncSession, book_id: UUID):
    statement = select(Book).options(   # type: ignore
        Load(Book).load_only(Book.user_id),   # type: ignore
    )
    statement = statement.where(Book.id == book_id)
    result = await session.execute(statement)
    try: 
        book = result.one()
        book = extract_object(object=book)
        return book
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no book with this ID: {book_id}')