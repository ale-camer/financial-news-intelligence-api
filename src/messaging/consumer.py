import json
import logging
from typing import Any

from confluent_kafka import Consumer, KafkaError

from src.api.config import settings

logger = logging.getLogger(__name__)


class MarketEventConsumer:
    """
    Kafka Consumer service for consuming raw market events from the market.events.raw topic.
    """

    def __init__(
        self,
        bootstrap_servers: str | None = None,
        topic: str | None = None,
        group_id: str | None = None,
        consumer: Consumer | None = None,
    ) -> None:
        self.bootstrap_servers = bootstrap_servers or settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = topic or settings.KAFKA_TOPIC_MARKET_EVENTS_RAW
        self.group_id = group_id or settings.KAFKA_GROUP_ID

        if consumer is not None:
            self.consumer = consumer
        else:
            self.consumer = Consumer(
                {
                    "bootstrap.servers": self.bootstrap_servers,
                    "group.id": self.group_id,
                    "auto.offset.reset": "earliest",
                }
            )

    def subscribe(self) -> None:
        """
        Subscribe consumer to the designated topic.
        """
        self.consumer.subscribe([self.topic])
        logger.info(
            f"Subscribed Kafka consumer to topic '{self.topic}' with group '{self.group_id}'"
        )

    def poll_events(self, timeout: float = 1.0, max_messages: int = 10) -> list[dict[str, Any]]:
        """
        Poll up to max_messages from Kafka and deserialize valid JSON market event payloads.
        """
        events: list[dict[str, Any]] = []
        count = 0

        while count < max_messages:
            msg = self.consumer.poll(timeout=timeout)
            if msg is None:
                break

            err = msg.error()
            if err is not None:
                if err.code() == KafkaError._PARTITION_EOF:
                    logger.debug(f"Reached end of partition for topic {msg.topic()}")
                else:
                    logger.error(f"Kafka consumer error: {err}")
                continue

            try:
                val = msg.value()
                if val is not None:
                    payload_str = val.decode("utf-8") if isinstance(val, bytes) else str(val)
                    event_data = json.loads(payload_str)
                    if isinstance(event_data, dict):
                        events.append(event_data)
                        count += 1
            except Exception as e:
                logger.warning(f"Error parsing message payload from Kafka: {e}")

        return events

    def close(self) -> None:
        """
        Close consumer connection gracefully.
        """
        try:
            self.consumer.close()
            logger.info("Kafka consumer closed successfully.")
        except Exception as e:
            logger.warning(f"Error closing Kafka consumer: {e}")
