from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings using Pydantic Settings."""

    PROJECT_NAME: str = "Financial News Intelligence API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///local.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
