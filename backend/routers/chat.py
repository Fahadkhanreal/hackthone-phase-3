from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict, Any

from auth.dependencies import get_current_user
from database import get_session
from agents.todo_agent import TodoAgent

router = APIRouter()


@router.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    message_data: Dict[str, Any],
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> Dict[str, Any]:
    """
    Chat endpoint that processes user messages through the AI agent

    Args:
        user_id: ID of the user making the request (must match JWT token)
        message_data: Contains 'message' and optional 'conversation_id'
        current_user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Dictionary with conversation_id, response, and tool_calls
    """
    # Verify that user_id in path matches user from JWT token
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="User ID in path does not match JWT token")

    # Extract message and optional conversation_id from request
    message = message_data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    conversation_id = message_data.get("conversation_id")

    # Get user's email from token - we need to get this differently
    # Since we only have the user ID, we'll need to fetch the email from the database
    from sqlmodel import select
    from models import User
    from uuid import UUID

    user_result = await session.exec(select(User).where(User.id == UUID(current_user_id)))
    current_user = user_result.first()

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_email = current_user.email

    # Create agent instance and process the message
    try:
        print(f"Processing message: '{message}' for user: {current_user_id}")

        agent = TodoAgent()
        result = await agent.process_message(
            session=session,
            user_id=current_user_id,
            user_email=user_email,
            message=message,
            conversation_id=conversation_id
        )

        print(f"Message processed successfully. Result: {result.get('response', 'No response text')[:50]}...")
        return result
    except ValueError as ve:
        # Handle specific value errors (like missing API key)
        import traceback
        print(f"Configuration error in chat processing: {str(ve)}")
        print(traceback.format_exc())

        raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        # Log the error for debugging
        import traceback
        print(f"Error in chat processing: {str(e)}")
        print(traceback.format_exc())

        # Return an error response to the client
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")