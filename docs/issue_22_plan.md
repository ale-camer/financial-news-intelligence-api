# Issue #22 — Kafka Consumer: market.events.raw (P-03 Integration)

**Branch**: `feature/issue-22-kafka-consumer`  
**Milestone**: M4 (Storage & Messaging)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to implement a Kafka consumer service that listens to the `market.events.raw` topic. This service ingests raw market tick and event data coming from external market data sources (such as P-03 integration), parsing incoming JSON payloads so they can be correlated with financial news sentiment analysis.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-22-kafka-consumer
```

### Step 2: Update Configuration

Add Consumer configuration settings.

1. Update `src/api/config.py`:
   - Add `KAFKA_GROUP_ID: str = "financial-news-group"`
   - Add `KAFKA_TOPIC_MARKET_EVENTS_RAW: str = "market.events.raw"`

### Step 3: Implement Kafka Consumer Service

Create the consumer service class.

1. Create `src/messaging/consumer.py`:
   - Define `MarketEventConsumer` class:
     - `__init__(self, bootstrap_servers: str | None = None, topic: str | None = None, group_id: str | None = None, consumer: Consumer | None = None)`
     - `subscribe(self) -> None`: Subscribes the Kafka consumer to `KAFKA_TOPIC_MARKET_EVENTS_RAW`.
     - `poll_events(self, timeout: float = 1.0, max_messages: int = 10) -> list[dict[str, Any]]`: Polls up to `max_messages` from Kafka, deserializes valid JSON payloads, handles `KafkaError` / EOF gracefully, and returns parsed market event dictionaries.
     - `close(self) -> None`: Gracefully closes the underlying consumer connection.

### Step 4: Write Unit Tests

Verify topic subscription, event polling, JSON parsing, error handling, and consumer closing using mocks.

1. Create `tests/unit/test_kafka_consumer.py`.
2. Use `unittest.mock.MagicMock` to mock the `confluent_kafka.Consumer` instance.
3. Test scenario coverage:
   - Subscription to `market.events.raw`.
   - Polling valid market event JSON messages.
   - Polling timeout (empty batch).
   - Kafka error handling (`KafkaError` handling).
   - Graceful consumer shutdown (`close`).

**Validation:**
Run pytest on the new unit test file.
```bash
pytest tests/unit/test_kafka_consumer.py -v
```

### Step 5: Code Quality & Formatting

Format the code and check static typing.

**Commands:**
```bash
ruff check src/messaging/ tests/unit/ --fix
ruff format src/messaging/ tests/unit/
mypy src/messaging/ tests/unit/
```

### Step 6: Commit and Push

Stage files, commit, and push the branch.

**Commands:**
```bash
git add docs/issue_22_plan.md src/api/config.py src/messaging/consumer.py tests/unit/test_kafka_consumer.py
git commit -m "feat(messaging): implement MarketEventConsumer for market.events.raw topic (Issue #22)"
git push -u origin feature/issue-22-kafka-consumer
```

### Step 7: Merge into Develop

Merge feature branch into `develop` and clean up.

**Commands:**
```bash
git checkout develop
git merge feature/issue-22-kafka-consumer
git branch -d feature/issue-22-kafka-consumer
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] Kafka consumer settings (`KAFKA_GROUP_ID`, `KAFKA_TOPIC_MARKET_EVENTS_RAW`) added to `src/api/config.py`.
- [ ] `MarketEventConsumer` implemented in `src/messaging/consumer.py`.
- [ ] Unit tests in `tests/unit/test_kafka_consumer.py` pass with full coverage.
- [ ] Zero Ruff or MyPy errors.
- [ ] Feature branch merged into `develop`.
