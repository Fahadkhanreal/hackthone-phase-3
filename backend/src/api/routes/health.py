from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict, Any
from sqlalchemy import text
from ...database.engine import get_async_session

router = APIRouter()

@router.get("/health", response_model=Dict[str, Any])
async def health_check(session: AsyncSession = Depends(get_async_session)) -> Dict[str, Any]:
    """
    Health check endpoint that confirms database connectivity
    """
    try:
        # Execute a simple query to test database connectivity
        result = await session.exec(text("SELECT 1"))
        # If we reach here, the database connection is working
        return {
            "status": "healthy",
            "db_connected": True,
            "message": "Database connection is established and operational"
        }
    except Exception as e:
        # If there's an error, return unhealthy status
        return {
            "status": "unhealthy",
            "db_connected": False,
            "error": f"Database connection failed: {str(e)}"
        }