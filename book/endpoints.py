from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, LimitOffsetPage

from user.schemas import User
from user.fast_users import fastapi_users
from book import services as book_services
from book.schemas import BookList, BookUpdate, BookRetrieve, BookCreateIn, BookCreateOut
from core.db import get_session


router = APIRouter()
current_user = fastapi_users.current_user(active=True, verified=True)
 
 
@router.get('', response_model = Page[BookList])
@router.get('/limit-offset', response_model = LimitOffsetPage[BookList])
async def book_list(session: AsyncSession = Depends(get_session), available: Optional[bool] = None):
    books = await book_services.get_books(session=session, available=available)
    return books


@router.get('/{book_id}', response_model=BookRetrieve)
async def book_retrieve(book_id: UUID, session: AsyncSession = Depends(get_session)):
    book = await book_services.get_book(session=session, book_id=book_id)
    return book


@router.post('/create', response_model=BookCreateOut)
async def book_create(
    item: BookCreateIn, 
    session: AsyncSession = Depends(get_session), 
    user: User = Depends(current_user)
):
    book = await book_services.insert_book(session=session, item=item, user_id=user.id)
    return book


@router.patch('/update/{book_id}')
async def update_book(
    book_id: UUID, 
    item: BookUpdate, 
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    book = await book_services.update_book(session=session, book_id=book_id, item=item, user_id=user.id)
    return book


@router.delete('/delete/{book_id}')
async def delete_book(book_id: UUID, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    book = await book_services.delete_book(session=session, book_id=book_id, user_id=user.id)
    return book