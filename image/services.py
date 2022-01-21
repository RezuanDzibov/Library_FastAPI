from uuid import UUID

from fastapi import Depends, BackgroundTasks, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound   # type: ignore

from image.schemas import BookImageCreate
from image.models import BookImage
from utils import write_file, extract_object


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


async def get_image(session: AsyncSession, image_id: UUID):
    statement = select(BookImage).options(load_only(BookImage.image_path))   # type: ignore
    statement = statement.where(BookImage.id == image_id)
    result = await session.execute(statement)
    try:
        image = result.one()
        image = extract_object(object=image)
        image_path = image.image_path
        return image_path
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no image with this ID: {image_id}')
    

async def get_image_info(session: AsyncSession, image_id: UUID):
    statement = select(BookImage).options(   # type: ignore
        load_only(
            BookImage.id, 
            BookImage.book_id,
            BookImage.title,
            BookImage.available,
            BookImage.created
        )
    )
    statement = statement.where(BookImage.id == image_id)
    result = await session.execute(statement)
    try:
        image = result.one()
        image = extract_object(object=image)
        return image
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no image with this ID: {image_id}')