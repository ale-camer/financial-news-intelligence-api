import json
from unittest.mock import MagicMock, patch

from src.messaging.producer import NewsEventProducer


def test_kafka_producer_publish_success() -> None:
    mock_producer = MagicMock()
    producer_service = NewsEventProducer(
        bootstrap_servers="localhost:9092",
        topic="test.topic",
        producer=mock_producer,
    )

    article_data = {
        "title": "Fed Rate Decision",
        "link": "https://example.com/fed",
        "sentiment_label": "neutral",
    }

    success = producer_service.publish_news_event(article_data)

    assert success is True
    mock_producer.produce.assert_called_once_with(
        topic="test.topic",
        key=b"https://example.com/fed",
        value=json.dumps(article_data).encode("utf-8"),
        callback=producer_service._delivery_report,
    )
    mock_producer.poll.assert_called_once_with(0)


def test_kafka_producer_publish_exception() -> None:
    mock_producer = MagicMock()
    mock_producer.produce.side_effect = Exception("Kafka queue full")

    producer_service = NewsEventProducer(producer=mock_producer)
    success = producer_service.publish_news_event({"title": "Test"})

    assert success is False


def test_kafka_producer_delivery_report_success() -> None:
    mock_producer = MagicMock()
    mock_msg = MagicMock()
    mock_msg.topic.return_value = "news.processed"
    mock_msg.partition.return_value = 0
    mock_msg.offset.return_value = 42

    producer_service = NewsEventProducer(producer=mock_producer)
    producer_service._delivery_report(None, mock_msg)


def test_kafka_producer_delivery_report_failure() -> None:
    mock_producer = MagicMock()

    producer_service = NewsEventProducer(producer=mock_producer)
    producer_service._delivery_report("Broker unavailable", None)


def test_kafka_producer_flush_and_close() -> None:
    mock_producer = MagicMock()
    mock_producer.flush.return_value = 0

    producer_service = NewsEventProducer(producer=mock_producer)
    flushed = producer_service.flush(timeout=5.0)

    assert flushed == 0
    mock_producer.flush.assert_called_once_with(timeout=5.0)

    producer_service.close()
    assert mock_producer.flush.call_count == 2


def test_kafka_producer_default_init() -> None:
    with patch("src.messaging.producer.Producer") as mock_producer_cls:
        producer_service = NewsEventProducer()
        assert producer_service.bootstrap_servers == "localhost:9092"
        mock_producer_cls.assert_called_once_with({"bootstrap.servers": "localhost:9092"})
