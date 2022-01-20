from fastapi import UploadFile, Form
from pydantic import BaseModel, UUID4, constr


class BookImageCreate(BaseModel):
    book_id: UUID4
    title: constr(max_length=255)  # type: ignore
    available: bool = True
    file: UploadFile
    
    @classmethod
    def as_form(
        cls, 
        book_id: UUID4 = Form(...),
        title: constr(max_length=255) = Form(...),   # type: ignore
        available: bool = Form(...),
        file: UploadFile = Form(...)
    ):
        return cls(book_id=book_id, title=title, available=available, file=file)    