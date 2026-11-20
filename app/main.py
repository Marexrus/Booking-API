from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import engine, Base
from app.database import models
from app.routers.bookings import router


# создает таблицы и индексы до запуска приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
def home():
    return {"message": "API is working"}
