# Issue #23 — Integration Tests: Storage & Messaging (M4 Milestone Closure)

**Branch**: `feature/issue-23-integration-tests`  
**Milestone**: M4 (Storage & Messaging)  
**Type**: `test`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to establish a comprehensive integration test suite for the M4 Storage & Messaging layer (MongoDB, Redis, and Kafka), verifying the end-to-end interaction between database persistence, caching, and event streaming. Completing this issue ensures 80%+ test coverage and merges the feature branch into `develop`.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-23-integration-tests
```

### Step 2: Implement Storage & Messaging Integration Tests

Create end-to-end integration tests combining MongoDB, Redis Cache, and Kafka Messaging components.

1. Create `tests/integration/test_storage_messaging.py`:
   - `test_article_storage_and_cache_pipeline`: Verifies saving an article to `ArticleRepository`, caching the result in `RedisCacheService`, and demonstrating cache hits/misses.
   - `test_news_event_publishing_and_consumption_pipeline`: Simulates event publishing with `NewsEventProducer` and parsing consumed events using `MarketEventConsumer`.
   - `test_cache_invalidation_and_mongodb_fallback`: Verifies fallback to MongoDB when Redis cache expires or is flushed.

### Step 3: Run Validation & Verify Code Coverage

Run full test suite (unit + integration) and static checkers to ensure test coverage >= 80%.

**Commands:**
```bash
ruff check src/ tests/ --fix
ruff format src/ tests/
mypy src/ tests/
pytest tests/unit/ tests/integration/ -v --cov=src --cov-report=term-missing
```

### Step 4: Commit and Push

Stage files, commit, and push the branch.

**Commands:**
```bash
git add docs/issue_23_plan.md tests/integration/test_storage_messaging.py
git commit -m "test(storage-messaging): add integration tests for MongoDB, Redis, and Kafka (Issue #23)"
git push -u origin feature/issue-23-integration-tests
```

### Step 5: Merge into Develop

Merge feature branch into `develop` and delete feature branch.

**Commands:**
```bash
git checkout develop
git merge feature/issue-23-integration-tests
git branch -d feature/issue-23-integration-tests
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] Integration tests added in `tests/integration/test_storage_messaging.py`.
- [ ] End-to-end pipeline tested (MongoDB persistence + Redis caching + Kafka event streaming).
- [ ] Overall test coverage across `src/` is >= 80%.
- [ ] Zero Ruff or MyPy errors.
- [ ] Feature branch merged into `develop`.
