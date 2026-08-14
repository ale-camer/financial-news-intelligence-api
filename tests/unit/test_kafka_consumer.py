import json
from unittest.mock import MagicMock, patch

from confluent_kafka import KafkaError

from src.messaging.consumer import MarketEventConsumer


def test_kafka_consumer_default_init() -> None:
    with patch("src.messaging.consumer.Consumer") as mock_consumer_cls:
        consumer_service = MarketEventConsumer()
        assert consumer_service.topic == "market.events.raw"
        mock_consumer_cls.assert_called_once_with(
            {
                "bootstrap.servers": "localhost:9092",
                "group.id": "financial-news-group",
                "auto.offset.reset": "earliest",
            }
        )


def test_kafka_consumer_subscribe() -> None:
    mock_consumer = MagicMock()
    consumer_service = MarketEventConsumer(topic="custom.topic", consumer=mock_consumer)
    consumer_service.subscribe()

    mock_consumer.subscribe.assert_called_once_with(["custom.topic"])


def test_kafka_consumer_poll_events_success() -> None:
    mock_consumer = MagicMock()
    mock_msg1 = MagicMock()
    mock_msg1.error.return_value = None
    mock_msg1.value.return_value = json.dumps({"symbol": "BTCUSD", "price": 50000.0}).encode(
        "utf-8"
    )

    mock_consumer.poll.side_effect = [mock_msg1, None]

    consumer_service = MarketEventConsumer(consumer=mock_consumer)
    events = consumer_service.poll_events(timeout=0.5, max_messages=5)

    assert len(events) == 1
    assert events[0] == {"symbol": "BTCUSD", "price": 50000.0}


def test_kafka_consumer_poll_events_partition_eof() -> None:
    mock_consumer = MagicMock()
    mock_msg = MagicMock()

    mock_error = MagicMock()
    mock_error.code.return_value = KafkaError._PARTITION_EOF
    mock_msg.error.return_value = mock_error
    mock_msg.topic.return_value = "market.events.raw"

    mock_consumer.poll.side_effect = [mock_msg, None]

    consumer_service = MarketEventConsumer(consumer=mock_consumer)
    events = consumer_service.poll_events(timeout=0.1, max_messages=5)

    assert len(events) == 0


def test_kafka_consumer_poll_events_kafka_error() -> None:
    mock_consumer = MagicMock()
    mock_msg = MagicMock()

    mock_error = MagicMock()
    mock_error.code.return_value = KafkaError._ALL_BROKERS_DOWN
    mock_msg.error.return_value = mock_error

    mock_consumer.poll.side_effect = [mock_msg, None]

    consumer_service = MarketEventConsumer(consumer=mock_consumer)
    events = consumer_service.poll_events(timeout=0.1, max_messages=5)

    assert len(events) == 0


def test_kafka_consumer_poll_events_invalid_json() -> None:
    mock_consumer = MagicMock()
    mock_msg = MagicMock()
    mock_msg.error.return_value = None
    mock_msg.value.return_value = b"invalid json content"

    mock_consumer.poll.side_effect = [mock_msg, None]

    consumer_service = MarketEventConsumer(consumer=mock_consumer)
    events = consumer_service.poll_events(timeout=0.1, max_messages=5)

    assert len(events) == 0


def test_kafka_consumer_close() -> None:
    mock_consumer = MagicMock()
    consumer_service = MarketEventConsumer(consumer=mock_consumer)
    consumer_service.close()

    mock_consumer.close.assert_called_once()


def test_kafka_consumer_close_exception() -> None:
    mock_consumer = MagicMock()
    mock_consumer.close.side_effect = Exception("Consumer error")

    consumer_service = MarketEventConsumer(consumer=mock_consumer)
    consumer_service.close()
