from fastapi import FastAPI
from fastapi_pagination import add_pagination

from routes import routes
from core.db import database


app = FastAPI(title='Library API')
app.include_router(routes)

add_pagination(app)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()