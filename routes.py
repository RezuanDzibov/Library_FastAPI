from fastapi import APIRouter

from book import endpoints as book_endpoints


routes = APIRouter()

routes.include_router(book_endpoints.router, prefix='/books')