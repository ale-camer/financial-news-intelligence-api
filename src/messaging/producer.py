import json
import logging
from collections.abc import Callable
from typing import Any

from confluent_kafka import Producer

from src.api.config import settings

logger = logging.getLogger(__name__)


class NewsEventProducer:
    """
    Kafka Producer service for publishing enriched news events to the news.processed topic.
    """

    def __init__(
        self,
        bootstrap_servers: str | None = None,
        topic: str | None = None,
        producer: Producer | None = None,
    ) -> None:
        self.bootstrap_servers = bootstrap_servers or settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = topic or settings.KAFKA_TOPIC_NEWS_PROCESSED
        if producer is not None:
            self.producer = producer
        else:
            self.producer = Producer({"bootstrap.servers": self.bootstrap_servers})

    def _delivery_report(self, err: Any, msg: Any) -> None:
        """
        Callback triggered on message delivery status from Kafka.
        """
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(
                f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
            )

    def publish_news_event(
        self,
        article_data: dict[str, Any],
        callback: Callable[[Any, Any], None] | None = None,
    ) -> bool:
        """
        Serialize article payload to JSON and send to the Kafka topic.
        """
        try:
            payload = json.dumps(article_data).encode("utf-8")
            key = str(article_data.get("link") or article_data.get("id") or "").encode("utf-8")
            on_delivery = callback or self._delivery_report

            self.producer.produce(
                topic=self.topic,
                key=key,
                value=payload,
                callback=on_delivery,
            )
            self.producer.poll(0)
            return True
        except Exception as e:
            logger.error(f"Failed to publish Kafka event to topic {self.topic}: {e}")
            return False

    def flush(self, timeout: float = 10.0) -> int:
        """
        Flush any outstanding messages in the producer queue.
        """
        return self.producer.flush(timeout=timeout)

    def close(self) -> None:
        """
        Flush remaining messages and close the producer.
        """
        self.flush()
