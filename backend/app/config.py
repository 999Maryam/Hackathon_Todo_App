
"""Configuration management for the backend API."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str
    """PostgreSQL connection string (required)."""

    # Authentication
    better_auth_secret: str
    """Shared secret key for JWT verification from Better Auth."""

    # AI Configuration - Google Gemini (legacy)
    gemini_api_key: str = ""
    """API key for Google Gemini AI service."""

    gemini_model: str = "gemini-1.5-flash"
    """Model name for Google Gemini AI service."""

    # AI Configuration - OpenRouter
    openrouter_api_key: str = ""
    """API key for OpenRouter AI service."""

    openrouter_model: str = "mistralai/devstral-2512:free"
    """Model name for OpenRouter AI service."""

    base_url: str = "https://openrouter.ai/api/v1"
    """Base URL for OpenRouter API."""

    # Optional Configuration
    jwt_expiry_days: int = 7
    """JWT token expiry time in days."""

    log_level: str = "INFO"
    """Logging level: DEBUG, INFO, WARNING, ERROR."""

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
