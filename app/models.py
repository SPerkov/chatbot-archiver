import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.schemas import Role


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    content = Column(String, nullable=False)
    rating = Column(Boolean, nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=False)
    role = Column(SAEnum(Role, name="role_enum"), nullable=False)
