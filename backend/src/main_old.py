from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from .database.engine import engine
from .api.routes.health import router as health_router
from .config.settings import settings
from .database.models.task import Task  # Import Task model to register it with SQLModel
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown
    """
    logger.info("Starting up...")
    # Initialize database tables on startup
    async with engine.begin() as conn:
        # Create all tables defined in SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created successfully")
    yield
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Todo Backend – Spec 1",
    description="Backend Database and ORM Setup for Multi-User Todo Web Application",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(health_router, prefix="", tags=["health"])

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {"message": "Todo Backend API - Database and ORM Setup"}