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
