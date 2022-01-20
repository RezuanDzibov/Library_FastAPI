import os
from pathlib import Path

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from routes import routes
from core.db import database
from config import BASE_DIR


app = FastAPI(title='Library API')
app.include_router(routes)

MEDIA = BASE_DIR.joinpath('media')

if not os.path.isdir(MEDIA):
    Path.mkdir(MEDIA)

add_pagination(app)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()