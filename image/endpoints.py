from email.mime import image
from fastapi import APIRouter, Depends, BackgroundTasks

from utils import write_file
from image.schemas import BookImageCreate


router = APIRouter()


@router.post('/create')
async def create_image(
    background_tasks: BackgroundTasks, 
    form: BookImageCreate = Depends(BookImageCreate.as_form)
):

    # background_tasks.add_task(write_file, file)
    return form.file.filename