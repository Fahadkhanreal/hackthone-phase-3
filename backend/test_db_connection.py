import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

# Load environment variables
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

print(f"Attempting to connect with URL: {DATABASE_URL}")

try:
    # Try to create the engine
    engine = create_async_engine(DATABASE_URL)
    print("Engine created successfully!")

    # Test the connection
    async def test_connection():
        async with engine.connect() as conn:
            print("Database connection successful!")
            result = await conn.execute("SELECT 1")
            print("Query executed successfully:", result.fetchone())

    import asyncio
    asyncio.run(test_connection())

except Exception as e:
    print(f"Error creating engine or connecting: {e}")
    print(f"Error type: {type(e)}")