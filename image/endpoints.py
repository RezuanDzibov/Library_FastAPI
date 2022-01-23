from uuid import UUID
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from user.fast_users import fastapi_users
from user.schemas import User
from image.schemas import BookImageCreate, BookImageRetrieve
from image import services as image_services


router = APIRouter()
current_user = fastapi_users.current_user(active=True, verified=True)


@router.post('/create', response_model=BookImageRetrieve)
async def create_image(
    background_tasks: BackgroundTasks, 
    form: BookImageCreate = Depends(BookImageCreate.as_form), 
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    image = await image_services.inaert_book_image(
        session=session, 
        background_tasks=background_tasks, 
        form=form,
        user_id=str(user.id)
    )
    return image


@router.get('/{image_id}', response_model=BookImageRetrieve)
async def image_retrieve(image_id: UUID, session: AsyncSession = Depends(get_session)):
    image = await image_services.get_book_image(session=session, image_id=image_id)
    return image


@router.get('/picture/{image_id}')
async def image_picture_retrieve(image_id: UUID, session: AsyncSession = Depends(get_session)):
    image_path = await image_services.get_book_image_picture(session=session, image_id=image_id)
    return FileResponse(image_path)


@router.delete('/delete/{book_id}/{image_id}', response_model=BookImageRetrieve, status_code=204)
async def image_delete(
    book_id: UUID,
    image_id: UUID, 
    background_tasks: BackgroundTasks, 
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    image = await image_services.delete_book_image(
        session=session, 
        background_tasks=background_tasks, 
        image_id=image_id,
        book_id=book_id,
        user_id=str(user.id)
)
    return image