import json
from typing import Any, cast
from unittest.mock import MagicMock

from bson import ObjectId

from src.messaging.consumer import MarketEventConsumer
from src.messaging.producer import NewsEventProducer
from src.storage.mongodb import ArticleRepository
from src.storage.redis_cache import RedisCacheService


def test_article_storage_and_cache_pipeline() -> None:
    """
    Integration test verifying MongoDB article persistence combined with Redis caching.
    """
    mock_mongo_client = MagicMock()
    mock_redis_client = MagicMock()

    dummy_oid = ObjectId()
    doc_in_db = {
        "_id": dummy_oid,
        "title": "Nvidia Quarterly Earnings",
        "link": "https://example.com/nvidia-earnings",
        "sentiment_label": "positive",
        "sentiment_score": 0.95,
    }

    mock_mongo_client["financial_news"]["articles"].find_one.return_value = doc_in_db

    repo = ArticleRepository(client=mock_mongo_client, db_name="financial_news")
    db_article = repo.get_article_by_id(str(dummy_oid))

    assert db_article is not None
    assert db_article["title"] == "Nvidia Quarterly Earnings"

    cache_key = f"article:{db_article['_id']}"
    mock_redis_client.get.return_value = None

    cache_service = RedisCacheService(client=mock_redis_client)
    assert cache_service.get(cache_key) is None

    saved_cache = cache_service.set(cache_key, db_article)
    assert saved_cache is True
    cast(MagicMock, mock_redis_client.set).assert_called_once()

    mock_redis_client.get.return_value = json.dumps(db_article)
    cached_article = cache_service.get(cache_key)

    assert cached_article is not None
    assert cached_article["title"] == "Nvidia Quarterly Earnings"


def test_news_event_publishing_and_consumption_pipeline() -> None:
    """
    Integration test simulating Kafka event publishing (producer) and market tick consumption (consumer).
    """
    mock_producer = MagicMock()
    mock_consumer = MagicMock()

    producer_service = NewsEventProducer(topic="news.processed", producer=mock_producer)
    news_payload = {
        "title": "Fed Announces Rate Cuts",
        "link": "https://example.com/fed-cut",
        "sentiment_label": "positive",
    }

    published = producer_service.publish_news_event(news_payload)
    assert published is True
    cast(MagicMock, mock_producer.produce).assert_called_once()

    mock_msg = MagicMock()
    mock_msg.error.return_value = None
    mock_msg.value.return_value = json.dumps(
        {"symbol": "SPY", "price": 510.50, "timestamp": "2026-08-14T20:00:00Z"}
    ).encode("utf-8")

    mock_consumer.poll.side_effect = [mock_msg, None]

    consumer_service = MarketEventConsumer(topic="market.events.raw", consumer=mock_consumer)
    consumer_service.subscribe()
    market_ticks = consumer_service.poll_events(timeout=0.5)

    assert len(market_ticks) == 1
    assert market_ticks[0]["symbol"] == "SPY"
    assert market_ticks[0]["price"] == 510.50


def test_cache_invalidation_and_mongodb_fallback() -> None:
    """
    Integration test validating Redis cache miss fallback to MongoDB and subsequent cache refresh.
    """
    mock_mongo_client = MagicMock()
    mock_redis_client = MagicMock()

    dummy_oid = ObjectId()
    doc_in_db = {
        "_id": dummy_oid,
        "title": "Apple Keynote Update",
        "link": "https://example.com/apple",
    }

    mock_mongo_client["financial_news"]["articles"].find_one.return_value = doc_in_db
    mock_redis_client.get.return_value = None

    cache_service = RedisCacheService(client=mock_redis_client)
    repo = ArticleRepository(client=mock_mongo_client, db_name="financial_news")

    cache_key = f"article:{str(dummy_oid)}"
    cached_data = cache_service.get(cache_key)

    if cached_data is None:
        article_from_db: dict[str, Any] | None = repo.get_article_by_id(str(dummy_oid))
        assert article_from_db is not None
        cache_service.set(cache_key, article_from_db)

    cast(MagicMock, mock_mongo_client["financial_news"]["articles"].find_one).assert_called_once()
    cast(MagicMock, mock_redis_client.set).assert_called_once()
