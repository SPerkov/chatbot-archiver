import os

# Must be set before app imports so pydantic-settings picks them up
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("API_KEY", "test-api-key")

from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.repository import AbstractMessageRepository
from app.routers.messages import get_repo
from app.schemas import MessageCreate, MessageResponse, MessageUpdate

TEST_API_KEY = "test-api-key"


class InMemoryMessageRepository(AbstractMessageRepository):
    def __init__(self):
        self._store: dict[UUID, MessageResponse] = {}

    async def create(self, data: MessageCreate) -> MessageResponse:
        response = MessageResponse(**data.model_dump())
        self._store[data.message_id] = response
        return response

    async def update(self, message_id: UUID, data: MessageUpdate) -> MessageResponse | None:
        if message_id not in self._store:
            return None
        msg = self._store[message_id]
        updated = msg.model_copy(update=data.model_dump(exclude_none=True))
        self._store[message_id] = updated
        return updated

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MessageResponse]:
        values = sorted(self._store.values(), key=lambda m: (m.sent_at, m.message_id))
        return values[skip : skip + limit]


@pytest.fixture
def repo():
    return InMemoryMessageRepository()


@pytest.fixture
async def client(repo):
    app.dependency_overrides[get_repo] = lambda: repo
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
