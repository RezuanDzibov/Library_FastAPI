from fastapi import APIRouter

from book.endpoints import router as book_router
from user.fast_users import fastapi_users, auth_backend
from image.endpoints import router as image_router


routes = APIRouter()

routes.include_router(book_router, prefix='/books', tags=['books'])
routes.include_router(image_router, prefix='/images', tags=['images'])
routes.include_router(fastapi_users.get_auth_router(auth_backend),  prefix='/users', tags=['users'])
routes.include_router(fastapi_users.get_register_router(), prefix='/users', tags=['users'])
routes.include_router(fastapi_users.get_users_router(auth_backend), prefix='/users', tags=['users']) # type: ignore
routes.include_router(fastapi_users.get_verify_router(), prefix='/users', tags=['users'])
routes.include_router(fastapi_users.get_reset_password_router(), prefix='/users', tags=['users'])