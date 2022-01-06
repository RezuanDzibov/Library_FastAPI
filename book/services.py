from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from book.models import BookModel
from book.schemas import BookUpdate, BookBase


async def get_books(session: AsyncSession, available: bool):
    statement = select(BookModel)
    if available is not None:
        statement = statement.where(BookModel.available == available)
    books = await session.execute(statement)
    books = books.scalars().all()
    return books


async def get_book(session: AsyncSession, book_id: str):
    statement = select(BookModel).where(BookModel.id == book_id)
    book = await session.execute(statement)
    book = book.scalar()
    return book


async def insert_book(session: AsyncSession, item: BookBase):
    book = BookModel(**item.dict())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def update_book(session: AsyncSession, book_id: str, item: BookUpdate):
    book = item.dict(exclude_unset=True)
    statement = update(BookModel).where(BookModel.id == book_id).values(**book)
    await session.execute(statement)
    await session.commit()
    statement = select(BookModel).where(BookModel.id == book_id)
    book = await session.execute(statement)
    book = book.scalar()
    return book


async def delete_book(session: AsyncSession, book_id: str):
    statement = select(BookModel).where(BookModel.id == book_id)
    book = await session.execute(statement)
    book = book.scalar()
    await session.delete(book)
    await session.commit()