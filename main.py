from fastapi import FastAPI

from core.db import database
from routes import routes
from core.fast_users import fastapi_users


app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

app.include_router(routes)
app.include_router(fastapi_users.get_register_router(), prefix='/users', tags=['users'])