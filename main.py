from fastapi import FastAPI

from routes import routes


app = FastAPI(title='Library API')
app.include_router(routes)