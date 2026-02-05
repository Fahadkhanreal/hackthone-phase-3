from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import models to ensure they're registered with SQLModel for table creation
from models import User, Task, Conversation, Message

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")  # Use test database as fallback

# Create async engine
engine: AsyncEngine = create_async_engine(DATABASE_URL)

# Session factory for async sessions
async def get_session():
    async with AsyncSession(engine) as session:
        yield session