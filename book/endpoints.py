from typing import Optional

from fastapi import APIRouter

from book import services as book_services
from book.schemas import BookUpdate, BookCreate

router = APIRouter()


@router.get('')
async def book_list(available: Optional[bool] = None):
    return await book_services.get_books(available=available)


@router.get('/{book_id}')
async def get_book(book_id: str):
    book = await book_services.get_book(book_id=book_id)
    return book


@router.post('/create')
async def book_create(item: BookCreate):
    return await book_services.insert_book(item=item)


@router.patch('/update/{book_id}')
async def update_book(book_id: str, item: BookUpdate):
    return await book_services.update_book(book_id=book_id, item=item)


@router.delete('/delete/(book_id)')
async def delete_book(book_id: str):
    await book_services.delete_book(book_id=book_id)