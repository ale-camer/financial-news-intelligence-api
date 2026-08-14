import json
from unittest.mock import MagicMock

from src.storage.redis_cache import RedisCacheService, get_redis_client


def test_get_redis_client() -> None:
    client = get_redis_client("redis://localhost:6379/0")
    assert client is not None


def test_redis_cache_get_hit() -> None:
    mock_client = MagicMock()
    mock_client.get.return_value = json.dumps({"title": "Test Article"})

    service = RedisCacheService(client=mock_client, default_ttl=300)
    data = service.get("article:1")

    assert data == {"title": "Test Article"}
    mock_client.get.assert_called_once_with("article:1")


def test_redis_cache_get_hit_bytes() -> None:
    mock_client = MagicMock()
    mock_client.get.return_value = json.dumps({"title": "Test Article"}).encode("utf-8")

    service = RedisCacheService(client=mock_client)
    data = service.get("article:1")

    assert data == {"title": "Test Article"}


def test_redis_cache_get_miss() -> None:
    mock_client = MagicMock()
    mock_client.get.return_value = None

    service = RedisCacheService(client=mock_client)
    data = service.get("article:nonexistent")

    assert data is None


def test_redis_cache_get_exception() -> None:
    mock_client = MagicMock()
    mock_client.get.side_effect = Exception("Connection error")

    service = RedisCacheService(client=mock_client)
    data = service.get("article:1")

    assert data is None


def test_redis_cache_set_default_ttl() -> None:
    mock_client = MagicMock()

    service = RedisCacheService(client=mock_client, default_ttl=600)
    success = service.set("article:1", {"title": "Test"})

    assert success is True
    mock_client.set.assert_called_once_with("article:1", json.dumps({"title": "Test"}), ex=600)


def test_redis_cache_set_custom_ttl() -> None:
    mock_client = MagicMock()

    service = RedisCacheService(client=mock_client, default_ttl=600)
    success = service.set("article:1", {"title": "Test"}, ttl=120)

    assert success is True
    mock_client.set.assert_called_once_with("article:1", json.dumps({"title": "Test"}), ex=120)


def test_redis_cache_set_exception() -> None:
    mock_client = MagicMock()
    mock_client.set.side_effect = Exception("Redis error")

    service = RedisCacheService(client=mock_client)
    success = service.set("article:1", {"title": "Test"})

    assert success is False


def test_redis_cache_delete_success() -> None:
    mock_client = MagicMock()
    mock_client.delete.return_value = 1

    service = RedisCacheService(client=mock_client)
    deleted = service.delete("article:1")

    assert deleted is True
    mock_client.delete.assert_called_once_with("article:1")


def test_redis_cache_delete_miss() -> None:
    mock_client = MagicMock()
    mock_client.delete.return_value = 0

    service = RedisCacheService(client=mock_client)
    deleted = service.delete("article:1")

    assert deleted is False


def test_redis_cache_delete_exception() -> None:
    mock_client = MagicMock()
    mock_client.delete.side_effect = Exception("Delete error")

    service = RedisCacheService(client=mock_client)
    deleted = service.delete("article:1")

    assert deleted is False


def test_redis_cache_flush_success() -> None:
    mock_client = MagicMock()

    service = RedisCacheService(client=mock_client)
    flushed = service.flush()

    assert flushed is True
    mock_client.flushdb.assert_called_once()


def test_redis_cache_flush_exception() -> None:
    mock_client = MagicMock()
    mock_client.flushdb.side_effect = Exception("Flush error")

    service = RedisCacheService(client=mock_client)
    flushed = service.flush()

    assert flushed is False
