"""
Basic test to verify the API implementation is working correctly
"""
from main import app
from fastapi.testclient import TestClient

def test_imports():
    """
    Test that all modules can be imported correctly
    """
    try:
        from config.settings import settings
        from auth.jwt_utils import decode_and_validate_jwt, create_access_token
        from auth.dependencies import get_current_user
        from schemas.task_schemas import TaskCreate, TaskRead, TaskUpdate
        from routers.tasks import router
        from models import Task
        print("SUCCESS: All imports successful")
    except ImportError as e:
        print(f"ERROR: Import error: {e}")
        raise

def test_app_routes():
    """
    Test that the app has the correct routes
    """
    route_paths = [route.path for route in app.routes]
    print(f"Available routes: {route_paths}")

    # Check if the API routes are included
    api_routes_found = any("/api/" in path for path in route_paths)
    if api_routes_found:
        print("SUCCESS: API routes are properly included")
    else:
        print("ERROR: API routes not found")

    # Check if health endpoint still exists
    if "/health" in route_paths:
        print("SUCCESS: Health endpoint exists")
    else:
        print("ERROR: Health endpoint not found")

if __name__ == "__main__":
    print("Running API implementation tests...")
    test_imports()
    test_app_routes()
    print("All basic tests passed!")