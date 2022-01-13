from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from book import services as book_services
from book.schemas import BookBase, BookUpdate, BookRetrieve
from core.db import get_session


router = APIRouter()


@router.get('', response_model=List[BookRetrieve])
async def book_list(session: AsyncSession = Depends(get_session), available: Optional[bool] = None):
    books = await book_services.get_books(session=session, available=available)
    return books


@router.get('/{book_id}', response_model=BookRetrieve)
async def book_retrieve(book_id: UUID, session: AsyncSession = Depends(get_session)):
    book = await book_services.get_book(session=session, book_id=book_id)
    return book


@router.post('/create', response_model=BookRetrieve)
async def book_create(item: BookBase, session: AsyncSession = Depends(get_session)):
    book = await book_services.insert_book(session=session, item=item)
    return book


@router.patch('/update/{book_id}')
async def update_book(book_id: UUID, item: BookUpdate, session: AsyncSession = Depends(get_session)):
    book = await book_services.update_book(session=session, book_id=book_id, item=item)
    return book


@router.delete('/delete/{book_id}')
async def delete_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    await book_services.delete_book(session=session, book_id=book_id)