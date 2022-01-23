from datetime import datetime
from uuid import UUID

from fastapi import Depends, BackgroundTasks, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound   # type: ignore

from book import services as book_services
from image.schemas import BookImageCreate
from image.models import BookImage
from core.utils import write_file, extract_object, delete_file, get_file_path


async def insert_image(
    session: AsyncSession,
    background_tasks: BackgroundTasks,
    user_id: str,
    form: BookImageCreate = Depends(BookImageCreate.as_form)
): 
    book = await book_services.get_book_user_id(session=session, book_id=form.book_id)
    if book.user_id != user_id:
        raise HTTPException(status_code=203, detail=f"Book with ID: {form.book_id.hex} doesn't belong you.")
    file = form.file
    filepath = f'media/{get_file_path(filename=file.filename)}'
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
    

async def delete_image(session: AsyncSession, background_tasks: BackgroundTasks, image_id: UUID, book_id, user_id: str):
    book = await book_services.get_book_user_id(session=session, book_id=book_id)
    if book.user_id != user_id:
        raise HTTPException(status_code=203, detail=f"Book with ID: {book_id.hex} doesn't belong you.")
    statement = delete(BookImage).where(BookImage.id == image_id).returning('*') # type: ignore
    try: 
        result = await session.execute(statement)
        await session.commit()
        image= result.one()
        background_tasks.add_task(delete_file, image.image_path)
        return image
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no image with this ID: {image_id}')