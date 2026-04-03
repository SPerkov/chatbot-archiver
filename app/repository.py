from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Message
from app.schemas import MessageCreate, MessageResponse, MessageUpdate


class AbstractMessageRepository(ABC):

    @abstractmethod
    async def create(self, data: MessageCreate) -> MessageResponse: ...

    @abstractmethod
    async def update(
        self, message_id: UUID, data: MessageUpdate
    ) -> MessageResponse | None: ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MessageResponse]: ...


class PostgresMessageRepository(AbstractMessageRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: MessageCreate) -> MessageResponse:
        row = Message(**data.model_dump())
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return MessageResponse.model_validate(row)

    async def update(
        self, message_id: UUID, data: MessageUpdate
    ) -> MessageResponse | None:
        row = await self._session.get(Message, message_id)
        if row is None:
            return None
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(row, field, value)
        await self._session.commit()
        await self._session.refresh(row)
        return MessageResponse.model_validate(row)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MessageResponse]:
        result = await self._session.execute(
            select(Message).order_by(Message.sent_at, Message.message_id).offset(skip).limit(limit)
        )
        return [MessageResponse.model_validate(row) for row in result.scalars()]
