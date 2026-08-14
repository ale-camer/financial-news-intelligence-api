# Issue #21 — Kafka Producer: news.processed Event Publishing

**Branch**: `feature/issue-21-kafka-producer`  
**Milestone**: M4 (Storage & Messaging)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to implement an asynchronous event publisher using Kafka to broadcast enriched news articles to the `news.processed` topic. This enables downstream microservices (such as market analytics and trade signals) to react in real-time to processed financial news events.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-21-kafka-producer
```

### Step 2: Install Dependencies & Update Configuration

Add Kafka messaging libraries and configuration settings.

1. Update `pyproject.toml` to include runtime dependency:
   - `confluent-kafka>=2.3.0`
2. Update `src/api/config.py`:
   - Add `KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"`
   - Add `KAFKA_TOPIC_NEWS_PROCESSED: str = "news.processed"`

### Step 3: Implement Kafka Event Producer

Create the messaging package and producer wrapper class.

1. Create `src/messaging/` directory and `src/messaging/__init__.py`.
2. Create `src/messaging/producer.py`:
   - Define `NewsEventProducer` class:
     - `__init__(self, bootstrap_servers: str | None = None, topic: str | None = None)`
     - `publish_news_event(self, article_data: dict[str, Any]) -> bool`: Serializes article data into JSON payload and produces message to `news.processed` topic using article link or ID as key.
     - `flush(self, timeout: float = 10.0) -> int`: Flushes pending messages.
     - `close(self) -> None`: Closes the underlying producer gracefully.

### Step 4: Write Unit Tests

Verify JSON serialization, event publishing, and error handling using mocks.

1. Create `tests/unit/test_kafka_producer.py`.
2. Use `unittest.mock.MagicMock` to mock the underlying Kafka Producer instance.
3. Test scenario coverage:
   - Successful payload delivery callback (`publish_news_event`).
   - Exception handling during serialization or connection failures.
   - Message key and topic targeting.
   - Producer `flush` and `close` execution.

**Validation:**
Run pytest on the new unit test file.
```bash
pytest tests/unit/test_kafka_producer.py -v
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
git add docs/issue_21_plan.md pyproject.toml src/api/config.py src/messaging/ tests/unit/test_kafka_producer.py
git commit -m "feat(messaging): implement NewsEventProducer for news.processed topic (Issue #21)"
git push -u origin feature/issue-21-kafka-producer
```

### Step 7: Merge into Develop

Merge feature branch into `develop` and clean up.

**Commands:**
```bash
git checkout develop
git merge feature/issue-21-kafka-producer
git branch -d feature/issue-21-kafka-producer
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `confluent-kafka>=2.3.0` added to `pyproject.toml`.
- [ ] Kafka settings (`KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC_NEWS_PROCESSED`) added to `src/api/config.py`.
- [ ] `NewsEventProducer` implemented in `src/messaging/producer.py`.
- [ ] Unit tests for Kafka producer in `tests/unit/test_kafka_producer.py` pass with high coverage.
- [ ] Zero Ruff or MyPy errors.
- [ ] Feature branch merged into `develop`.
