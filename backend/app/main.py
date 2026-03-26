from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from app.core.database import create_db_and_tables
from app.api.routers import upload, save

@asynccontextmanager
async def lifespan(app : FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)

app.include_router(upload.router)
app.include_router(save.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    message = exc.errors()[0]["msg"]
    new_message = message.replace("Value error, ", "")
    return JSONResponse(
        status_code = 422,
        content= jsonable_encoder({"detail": new_message}),
    )

