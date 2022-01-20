from fastapi import Depends, BackgroundTasks
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from image.schemas import BookImageCreate
from image.models import BookImage
from utils import write_file


async def insert_image(
    session: AsyncSession,
    background_tasks: BackgroundTasks, 
    form: BookImageCreate = Depends(BookImageCreate.as_form)
):
    file = form.file
    filepath = f"media/{file.filename}"
    form_data = form.dict()
    form_data['book_id'] = form_data['book_id'].hex
    form_data['image_path'] = filepath
    del form_data['file']
    statement = insert(BookImage).values(form_data).returning(
        BookImage.id, 
        BookImage.book_id, 
        BookImage.title,
        BookImage.available, 
        BookImage.created
    )
    result = await session.execute(statement)
    await session.commit()
    image = result.one()
    background_tasks.add_task(write_file, filepath, file)
    return image