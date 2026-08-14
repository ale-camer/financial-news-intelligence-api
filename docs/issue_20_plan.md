# Issue #20 — Redis Cache Layer: Recent Results TTL

**Branch**: `feature/issue-20-redis-cache`  
**Milestone**: M4 (Storage & Messaging)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to implement a Redis caching layer to cache query results, frequent articles, and sentiment metrics with a configurable Time-To-Live (TTL). This reduces database load and speeds up API response times by serving pre-computed JSON responses from in-memory Redis storage.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-20-redis-cache
```

### Step 2: Install Dependencies & Update Configuration

Add Redis client library and configuration settings.

1. Update `pyproject.toml` to include runtime dependency:
   - `redis>=5.0.0`
2. Update `src/api/config.py`:
   - Add `REDIS_URL: str = "redis://localhost:6379/0"`
   - Add `REDIS_CACHE_TTL: int = 3600` (1 hour default TTL)

### Step 3: Implement Redis Cache Service

Create the Redis client helper and caching wrapper class.

1. Create `src/storage/redis_cache.py`:
   - Implement `get_redis_client(url: str | None = None) -> Redis`: Client factory helper.
   - Define `RedisCacheService` class:
     - `__init__(self, client: Redis | None = None, default_ttl: int | None = None)`
     - `get(self, key: str) -> Any | None`: Gets raw string value from Redis, deserializes from JSON, returns data or `None` on cache miss / error.
     - `set(self, key: str, value: Any, ttl: int | None = None) -> bool`: Serializes object to JSON and stores in Redis with expiration (`ex=ttl`).
     - `delete(self, key: str) -> bool`: Removes key from Redis cache.
     - `flush(self) -> bool`: Flushes cache namespace or database.

### Step 4: Write Unit Tests

Verify caching logic, JSON serialization, TTL settings, and error handling using mocks.

1. Create `tests/unit/test_redis_cache.py`.
2. Use `unittest.mock.MagicMock` to mock Redis client calls (`get`, `set`, `delete`, `flushdb`).
3. Test scenario coverage:
   - Cache hit (`get` returning deserialized JSON).
   - Cache miss (`get` returning `None`).
   - `set` storing serialized JSON with explicit/default TTL.
   - `delete` and `flush` execution.
   - Handling invalid JSON gracefully.

**Validation:**
Run pytest on the new unit test file.
```bash
pytest tests/unit/test_redis_cache.py -v
```

### Step 5: Code Quality & Formatting

Run static checks to maintain quality standards.

**Commands:**
```bash
ruff check src/storage/ tests/unit/ --fix
ruff format src/storage/ tests/unit/
mypy src/storage/ tests/unit/
```

### Step 6: Commit and Push

Stage files, commit, and push the branch.

**Commands:**
```bash
git add docs/issue_20_plan.md pyproject.toml src/api/config.py src/storage/redis_cache.py tests/unit/test_redis_cache.py
git commit -m "feat(storage): implement RedisCacheService with TTL support (Issue #20)"
git push -u origin feature/issue-20-redis-cache
```

### Step 7: Merge into Develop

Merge the feature branch into `develop` and delete the feature branch.

**Commands:**
```bash
git checkout develop
git merge feature/issue-20-redis-cache
git branch -d feature/issue-20-redis-cache
git push origin develop
```

### Step 8: Merge Develop into Main

Promote the stable, tested code to `main`.

**Commands:**
```bash
git checkout main
git pull origin main
git merge develop
git push origin main
git checkout develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `redis>=5.0.0` dependency added to `pyproject.toml`.
- [ ] Redis settings (`REDIS_URL`, `REDIS_CACHE_TTL`) added to `src/api/config.py`.
- [ ] `RedisCacheService` implemented in `src/storage/redis_cache.py` with get/set/delete/flush methods.
- [ ] Full unit test coverage in `tests/unit/test_redis_cache.py`.
- [ ] Zero Ruff or MyPy errors.
- [ ] Feature branch merged into `develop`, and `develop` merged into `main`.
