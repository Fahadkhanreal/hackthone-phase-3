from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from sqlalchemy import text
from dotenv import load_dotenv
from database import engine
from models import Task

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown
    """
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Tables created successfully!")
    yield

# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include task router with prefix "/api"
from routers.tasks import router as tasks_router
app.include_router(tasks_router, prefix="/api")

# Include auth router
from routers.auth import router as auth_router
app.include_router(auth_router)

# Include chat router
from routers.chat import router as chat_router
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Todo Backend API - Secure Task Management"}

@app.get("/health")
async def health():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}