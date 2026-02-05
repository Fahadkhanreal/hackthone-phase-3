from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from models import Conversation, Message, User


async def create_conversation(session: AsyncSession, user_id: UUID) -> Conversation:
    """Create a new conversation for a user"""
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def get_conversation_by_id(session: AsyncSession, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
    """Get a conversation by ID for a specific user (ensuring user owns the conversation)"""
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await session.exec(statement)
    return result.first()


async def get_messages_for_conversation(session: AsyncSession, conversation_id: UUID, user_id: UUID) -> List[Message]:
    """Get all messages for a conversation, ensuring user owns the conversation"""
    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id
    ).order_by(Message.created_at.asc())
    result = await session.exec(statement)
    return result.all()


async def save_user_message(session: AsyncSession, conversation_id: UUID, user_id: UUID, content: str) -> Message:
    """Save a user message to the conversation"""
    message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="user",
        content=content
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def save_assistant_message(session: AsyncSession, conversation_id: UUID, user_id: UUID, content: str) -> Message:
    """Save an assistant message to the conversation"""
    message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="assistant",
        content=content
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message