from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv
from pydantic import Field, ConfigDict

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    database_url: str = Field(default="sqlite+aiosqlite:///./test.db", alias="DATABASE_URL")
    better_auth_secret: str = Field(default="dev-secret-key-change-in-production", alias="BETTER_AUTH_SECRET")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,  # Environment variables are typically not case-sensitive
        extra="ignore"  # This will ignore extra fields
    )


# Create settings instance
settings = Settings()