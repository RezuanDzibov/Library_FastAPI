from fastapi import APIRouter, UploadFile, File, BackgroundTasks

from utils import write_file


router = APIRouter()


@router.post('/create')
async def create_image(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    background_tasks.add_task(write_file, file)