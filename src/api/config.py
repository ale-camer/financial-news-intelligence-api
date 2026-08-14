from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings using Pydantic Settings."""

    PROJECT_NAME: str = "Financial News Intelligence API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///local.db"
    NEWSAPI_KEY: str = "test_key"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "financial_news"
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_NEWS_PROCESSED: str = "news.processed"
    KAFKA_GROUP_ID: str = "financial-news-group"
    KAFKA_TOPIC_MARKET_EVENTS_RAW: str = "market.events.raw"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
