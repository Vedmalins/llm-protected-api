from sqlalchemy import delete, select
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.chat import ChatMessage
from app.schemas.chat import ChatMessageSchema, ChatRequestSchema, ChatResponseSchema
from app.services.chat_service import save_message
from app.services.openrouter_service import get_llm_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponseSchema)
async def chat(
    data: ChatRequestSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_message = data.message
    assistant_message = await get_llm_response(data.message)

    await save_message(db, current_user.id, "user", user_message)
    await save_message(db, current_user.id, "assistant", assistant_message)

    return ChatResponseSchema(
        user_message=user_message,
        assistant_message=assistant_message,
    )

@router.get("/history", response_model=list[ChatMessageSchema])
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.id)
    )
    messages = result.scalars().all()
    return messages

@router.delete("/history")
async def clear_chat_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await db.execute(
        delete(ChatMessage).where(ChatMessage.user_id == current_user.id)
    )
    await db.commit()

    return {"detail": "Chat history cleared"}
