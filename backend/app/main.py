from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from app.core.database import create_db_and_tables
from app.api.routers import upload

@asynccontextmanager
async def lifespan(app : FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)

app.include_router(upload.router)




