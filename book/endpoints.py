from typing import Optional, List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from book import services as book_services
from book.schemas import BookBase, BookUpdate, BookRetrieve
from core.db import get_session


router = APIRouter()


@router.get('', response_model=List[BookRetrieve])
async def book_list(session: AsyncSession = Depends(get_session), available: Optional[bool] = None):
    return await book_services.get_books(session=session, available=available)


@router.get('/{book_id}', response_model=BookRetrieve)
async def book_retrieve(book_id: str, session: AsyncSession = Depends(get_session)):
    book = await book_services.get_book(session=session, book_id=book_id)
    return book


@router.post('/create', response_model=BookRetrieve)
async def book_create(item: BookBase, session: AsyncSession = Depends(get_session)):
    return await book_services.insert_book(session=session, item=item)


@router.patch('/update/{book_id}', response_model=BookRetrieve)
async def update_book(book_id: str, item: BookUpdate, session: AsyncSession = Depends(get_session)):
    return await book_services.update_book(session=session, book_id=book_id, item=item)


@router.delete('/delete/{book_id}')
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)):
    await book_services.delete_book(session=session, book_id=book_id)