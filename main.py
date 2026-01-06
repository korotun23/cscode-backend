from fastapi import FastAPI
from app.api.routes import database
from app.api.routes import preview

app = FastAPI()

app.include_router(database.router)
app.include_router(preview.router)