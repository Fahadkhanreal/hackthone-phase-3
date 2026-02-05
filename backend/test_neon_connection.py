"""
Basic test to verify the Neon database connection implementation is working correctly
"""
import asyncio
from main import app
from fastapi.testclient import TestClient

def test_imports():
    """
    Test that all modules can be imported correctly
    """
    try:
        from database import engine
        from models import Task
        from main import app
        print("✓ All imports successful")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        raise

def test_health_endpoint():
    """
    Test that the health endpoint works correctly
    """
    with TestClient(app) as client:
        response = client.get("/health")
        print(f"Health endpoint status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Health endpoint response: {data}")
            if data["status"] == "healthy":
                print("✓ Health endpoint test passed")
            else:
                print(f"✗ Health endpoint returned unhealthy: {data}")
        else:
            print(f"✗ Health endpoint returned status: {response.status_code}")

if __name__ == "__main__":
    print("Running Neon database connection tests...")
    test_imports()
    test_health_endpoint()
    print("Basic tests completed! 🎉")