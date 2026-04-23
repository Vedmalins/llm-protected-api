from contextlib import asynccontextmanager
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.chat import router as chat_router

from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {
        "message": "API is running",
        "app_name": settings.app_name,
    }
