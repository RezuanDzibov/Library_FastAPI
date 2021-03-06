from uuid import UUID
from typing import Union

from fastapi import Depends, BackgroundTasks, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound   # type: ignore

from book import services as book_services
from image.schemas import BookImageCreate, AvatarImageCreate
from image.models import BookImage, AvatarImage
from core.utils import write_file, extract_object, delete_file, get_file_path


class InsertBookImage:
    async def _validate_book_user_id(self, session, user_id, form):
        book = await book_services.get_book_user_id(session=session, book_id=form.book_id)
        if book.user_id != user_id:
            raise HTTPException(status_code=203, detail=f"Book with ID: {form.book_id.hex} doesn't belong you.")

    async def _process_form(self, form):
        file = form.file
        filepath = f'media/{get_file_path(filename=file.filename)}'
        form_data = form.dict()
        form_data['book_id'] = form_data['book_id'].hex
        form_data['image_path'] = filepath
        del form_data['file']
        return file, filepath, form_data

    async def _insert_image(self, session, form_data):
        statement = insert(BookImage).values(form_data).returning(
            BookImage.id,
            BookImage.book_id,
            BookImage.title,
            BookImage.available,
            BookImage.created_at
        )
        result = await session.execute(statement)
        await session.commit()
        image = result.one()
        return image

    async def __call__(
            self,
            session: AsyncSession,
            background_tasks: BackgroundTasks,
            user_id: str,
            form: BookImageCreate = Depends(BookImageCreate.as_form)
    ):
        await self._validate_book_user_id(session=session, user_id=user_id, form=form)
        file, filepath, form_data = await self._process_form(form=form)
        image = await self._insert_image(session=session, form_data=form_data)
        background_tasks.add_task(write_file, filepath, file)
        return image


async def get_image_picture(session: AsyncSession, image_id: UUID, image_model: Union[BookImage, AvatarImage]):
    statement = select(image_model).options(load_only(image_model.image_path))   # type: ignore
    statement = statement.where(image_model.id == image_id)
    result = await session.execute(statement)
    try:
        image = result.one()
        image = extract_object(object=image)
        image_path = image.image_path
        return image_path
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no image with this ID: {image_id}')
    

async def get_book_image(session: AsyncSession, image_id: UUID):
    statement = select(BookImage).options(   # type: ignore
        load_only(
            BookImage.id, 
            BookImage.book_id,
            BookImage.title,
            BookImage.available,
            BookImage.created_at
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
    

async def delete_book_image(session: AsyncSession, background_tasks: BackgroundTasks, image_id: UUID, book_id, user_id: str):
    book = await book_services.get_book_user_id(session=session, book_id=book_id)
    if book.user_id != user_id:
        raise HTTPException(status_code=203, detail=f"Book with ID: {book_id.hex} doesn't belong you.")
    statement = delete(BookImage).where(BookImage.id == image_id).returning('*')  # type: ignore
    try: 
        result = await session.execute(statement)
        await session.commit()
        image = result.one()
        background_tasks.add_task(delete_file, image.image_path)
        return image
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no image with this ID: {image_id}')
    

async def insert_avatar_image(
    session: AsyncSession,
    background_tasks: BackgroundTasks,
    user_id: str,
    form: AvatarImageCreate = Depends(AvatarImageCreate.as_form)
):
    file = form.file
    filepath = f'media/{get_file_path(filename=file.filename)}'
    form_data = form.dict()
    form_data['user_id'] = user_id
    form_data['image_path'] = filepath
    del form_data['file']
    statement = insert(AvatarImage).values(form_data).returning(
        AvatarImage.id, 
        AvatarImage.user_id, 
        AvatarImage.title,
        AvatarImage.available, 
        AvatarImage.created_at
    )
    result = await session.execute(statement)
    await session.commit()
    image = result.one()
    background_tasks.add_task(write_file, filepath, file)
    return image


async def get_avatar_image(session: AsyncSession, image_id: UUID):
    statement = select(AvatarImage).options(   # type: ignore
        load_only(
            AvatarImage.id,
            AvatarImage.user_id,
            AvatarImage.title,
            AvatarImage.available,
            AvatarImage.created_at
        )
    )
    statement = statement.where(AvatarImage.id == image_id)
    result = await session.execute(statement)
    try:
        image = result.one()
        image = extract_object(object=image)
        return image
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no image with this ID: {image_id}')


async def delete_avatar_image(session: AsyncSession, image_id: UUID, user_id: UUID):
    statement = delete(AvatarImage).where(AvatarImage.id == image_id, AvatarImage.user_id == user_id.hex).returning(   # type: ignore
        AvatarImage.id,
        AvatarImage.user_id,
        AvatarImage.title,
        AvatarImage.available,
        AvatarImage.created_at
    )
    try:
        result = await session.execute(statement)
        await session.commit()
        image = result.one()
        return image
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f'There is no image with this ID: {image_id} which belongs you')