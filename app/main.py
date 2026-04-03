from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers.messages import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: create tables if they don't exist yet
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown: release all pooled connections cleanly
    await engine.dispose()


app = FastAPI(
    title="Chatbot Archiver",
    description="Persists AI assistant messages to PostgreSQL.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)
