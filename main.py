from fastapi import FastAPI

from routes import routes
from core.db import database


app = FastAPI(title='Library API')
app.include_router(routes)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()