import json
import logging
from typing import Any

from redis import Redis

from src.api.config import settings

logger = logging.getLogger(__name__)


def get_redis_client(url: str | None = None) -> Redis:
    """
    Get Redis client instance from connection URL.
    """
    redis_url = url or settings.REDIS_URL
    return Redis.from_url(redis_url, decode_responses=True)


class RedisCacheService:
    """
    Service wrapper for managing in-memory caching with Redis and TTL.
    """

    def __init__(
        self,
        client: Redis | None = None,
        default_ttl: int | None = None,
    ) -> None:
        self.client = client or get_redis_client()
        self.default_ttl = default_ttl if default_ttl is not None else settings.REDIS_CACHE_TTL

    def get(self, key: str) -> Any | None:
        """
        Get value from Redis cache by key and deserialize JSON.
        Returns None on cache miss or deserialization error.
        """
        try:
            val = self.client.get(key)
            if val is None:
                return None
            if isinstance(val, bytes):
                val = val.decode("utf-8")
            return json.loads(val)
        except Exception as e:
            logger.warning(f"Error reading from Redis key '{key}': {e}")
            return None

    def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        """
        Serialize value to JSON and store in Redis with TTL in seconds.
        """
        try:
            expiration = ttl if ttl is not None else self.default_ttl
            serialized = json.dumps(value)
            self.client.set(key, serialized, ex=expiration)
            return True
        except Exception as e:
            logger.warning(f"Error setting Redis key '{key}': {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete key from Redis cache.
        """
        try:
            deleted_count = self.client.delete(key)
            return int(deleted_count) > 0
        except Exception as e:
            logger.warning(f"Error deleting Redis key '{key}': {e}")
            return False

    def flush(self) -> bool:
        """
        Flush all keys in the current Redis database.
        """
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            logger.warning(f"Error flushing Redis database: {e}")
            return False
