from uuid import UUID
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from image.schemas import BookImageCreate, BookImageRetrieve
from image import services as image_services


router = APIRouter()


@router.post('/create', response_model=BookImageRetrieve)
async def create_image(
    background_tasks: BackgroundTasks, 
    form: BookImageCreate = Depends(BookImageCreate.as_form), 
    session: AsyncSession = Depends(get_session)
):
    image = await image_services.insert_image(
        session=session, 
        background_tasks=background_tasks, 
        form=form
    )
    return image


@router.get('/{image_id}')
async def image_retrieve(image_id: UUID, session: AsyncSession = Depends(get_session)):
    image_path = await image_services.get_image(session=session, image_id=image_id)
    return FileResponse(image_path)


@router.get('/info/{image_id}', response_model=BookImageRetrieve)
async def image_retrieve_info(image_id: UUID, session: AsyncSession = Depends(get_session)):
    image = await image_services.get_image_info(session=session, image_id=image_id)
    return image


@router.delete('/{image_id}', response_model=BookImageRetrieve)
async def image_delete(image_id: UUID, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    image = await image_services.delete_image(session=session, background_tasks=background_tasks, image_id=image_id)
    return image