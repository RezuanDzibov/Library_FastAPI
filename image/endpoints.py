from uuid import UUID

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from user.fast_users import fastapi_users
from user.schemas import User
from image.schemas import BookImageCreate, BookImageRetrieve, AvatarImageCreate, AvatarImageRetrieve
from image import services as image_services
from image.models import AvatarImage, BookImage
from image.dataclasses import ImageType


router = APIRouter()
current_user = fastapi_users.current_user(active=True, verified=True)


@router.post('/book/create', response_model=BookImageRetrieve)
async def book_image_create(
    background_tasks: BackgroundTasks, 
    form: BookImageCreate = Depends(BookImageCreate.as_form), 
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    image = await image_services.insert_book_image(
        session=session, 
        background_tasks=background_tasks, 
        form=form,
        user_id=str(user.id)
    )
    return image


@router.get('/book/{image_id}', response_model=BookImageRetrieve)
async def book_image_retrieve(image_id: UUID, session: AsyncSession = Depends(get_session)):
    image = await image_services.get_book_image(session=session, image_id=image_id)
    return image


@router.get('/picture/{image_type}/{image_id}')
async def book_image_picture_retrieve(image_id: UUID, image_type: ImageType, session: AsyncSession = Depends(get_session)):
    if image_type == ImageType.avatar:
        image_path = await image_services.get_image_picture(session=session, image_id=image_id, image_model=AvatarImage)
    elif image_type == ImageType.book:
        image_path = await image_services.get_image_picture(session=session, image_id=image_id, image_model=BookImage)
    return FileResponse(image_path)


@router.delete('/delete/book/{book_id}/{image_id}', response_model=BookImageRetrieve)
async def book_image_delete(
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


@router.post('/avatar/create', response_model=AvatarImageRetrieve)
async def avatar_image_create(
    background_tasks: BackgroundTasks, 
    form: AvatarImageCreate = Depends(AvatarImageCreate.as_form), 
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    image = await image_services.insert_avatar_image(
        session=session, 
        background_tasks=background_tasks, 
        form=form,
        user_id=str(user.id)
    )
    return image


@router.get('/avatar/{image_id}', response_model=AvatarImageRetrieve)
async def avatar_image_retrieve(image_id: UUID, session: AsyncSession = Depends(get_session)):
    image = await image_services.get_avatar_image(session=session, image_id=image_id)
    return image