from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repository import AbstractMessageRepository, PostgresMessageRepository
from app.schemas import MessageCreate, MessageResponse, MessageUpdate
from app.security import verify_api_key

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[Depends(verify_api_key)],
)


def get_repo(db: AsyncSession = Depends(get_db)) -> AbstractMessageRepository:
    return PostgresMessageRepository(db)


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    payload: MessageCreate,
    repo: AbstractMessageRepository = Depends(get_repo),
):
    return await repo.create(payload)


@router.patch("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: UUID,
    payload: MessageUpdate,
    repo: AbstractMessageRepository = Depends(get_repo),
):
    updated = await repo.update(message_id, payload)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    return updated


@router.get("", response_model=list[MessageResponse])
async def list_messages(
    skip: int = 0,
    limit: int = 100,
    repo: AbstractMessageRepository = Depends(get_repo),
):
    return await repo.get_all(skip=skip, limit=limit)
