from fastapi import APIRouter, Depends, BackgroundTasks
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