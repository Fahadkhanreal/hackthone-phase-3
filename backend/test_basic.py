"""
Basic test to verify the backend implementation is working correctly
"""
import asyncio
from src.main import app
from src.database.engine import engine, get_async_session
from src.database.models.task import Task
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.testclient import TestClient

def test_health_endpoint():
    """
    Test that the health endpoint works correctly
    """
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["db_connected"] is True
        print("✓ Health endpoint test passed")

def test_imports():
    """
    Test that all modules can be imported correctly
    """
    try:
        from src.config.settings import settings
        from src.database.engine import engine, get_async_session
        from src.database.models.task import Task, TaskCreate, TaskRead
        from src.api.routes.health import router
        print("✓ All imports successful")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        raise

if __name__ == "__main__":
    print("Running basic tests...")
    test_imports()
    test_health_endpoint()
    print("All basic tests passed! 🎉")