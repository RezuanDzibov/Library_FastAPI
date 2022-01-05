from book.models import books
from book.schemas import BookUpdate, BookCreate
from core.db import database
from core.utils import generate_uuid


async def get_books(available):
    query = books.select()
    if available is not None:
        query = query.where(books.c.available == available)
    return await database.fetch_all(query)


async def get_book(book_id: str):
    query = books.select().where(books.c.id == book_id)
    book = await database.fetch_one(query)
    return book


async def insert_book(item: BookCreate):
    book = item.dict()
    book['id'] = await generate_uuid()
    query = books.insert().values(**book)
    book = await database.fetch_one(query=query)
    return book


async def update_book(book_id: str, item: BookUpdate):
    book = books.update().where(books.c.id == book_id).values(**item.dict(exclude_unset=True))
    result = await database.fetch_one(book)
    return result


async def delete_book(book_id: str):
    return await database.execute(books.delete().where(books.c.id == book_id))