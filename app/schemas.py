from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Role(str, Enum):
    ai = "ai"
    user = "user"


class MessageCreate(BaseModel):
    message_id: UUID
    chat_id: UUID
    content: str
    rating: bool
    sent_at: datetime
    role: Role


class MessageUpdate(BaseModel):
    content: str | None = None
    rating: bool | None = None


class MessageResponse(MessageCreate):
    # from_attributes=True lets Pydantic read SQLAlchemy ORM objects directly
    model_config = ConfigDict(from_attributes=True)
