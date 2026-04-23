from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import ChatMessage


async def save_message(
    db: AsyncSession,
    user_id: int,
    role: str,
    content: str,
) -> ChatMessage:
    message = ChatMessage(
        user_id=user_id,
        role=role,
        content=content,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message