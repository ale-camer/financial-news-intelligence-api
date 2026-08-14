# Issue #18 — Integration Tests: API Endpoints (httpx)

**Branch**: `feature/issue-18-api-integration-tests`  
**Milestone**: M3 (API Layer)  
**Type**: `test`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to finalize **Milestone 3 (API Layer)** by writing comprehensive integration tests for all API endpoints (`/health`, `GET /articles`, `GET /articles/{id}/sentiment`, `POST /ingest/trigger`, and middleware/error handling). Tests will use `httpx.AsyncClient` alongside an isolated in-memory SQLite database session fixture to verify the HTTP endpoints end-to-end. Once verified, we will merge the completed M3 milestone into `main`.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-18-api-integration-tests
```

### Step 2: Create Integration Scaffolding & Fixtures

Set up the integration test environment with isolated database sessions.

1. Create `tests/integration/` directory if not present.
2. Create `tests/integration/conftest.py`:
   - Define a fixture for an in-memory SQLite engine (`sqlite:///:memory:`).
   - Create tables using `SQLModel.metadata.create_all` / `Base.metadata.create_all`.
   - Provide a `db_session` fixture.
   - Override `get_session` in `app.dependency_overrides`.
   - Provide an `async_client` fixture using `httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")`.

### Step 3: Write API Integration Tests

Create end-to-end endpoint tests in `tests/integration/test_api_endpoints.py`.

1. `test_health_integration`:
   - Send `GET /health` with `async_client`.
   - Assert status 200, expected payload, and presence of `X-Process-Time` header.
2. `test_articles_list_and_filter_integration`:
   - Seed in-memory database with test articles.
   - Send `GET /api/v1/articles?sentiment_label=positive&limit=5`.
   - Assert returned list matches filtered data.
3. `test_article_sentiment_detail_integration`:
   - Send `GET /api/v1/articles/1/sentiment` for existing article -> Assert 200 OK.
   - Send `GET /api/v1/articles/999/sentiment` -> Assert 404 Not Found.
4. `test_ingest_trigger_integration`:
   - Mock external fetch (`run_ingestion`) and NLP (`process_batch`).
   - Send `POST /api/v1/ingest/trigger`.
   - Assert status 200 and verify articles are actually queried back from the database.

### Step 4: Validate Test Suite

Run the integration tests and check overall test coverage.

**Commands:**
```bash
pytest tests/integration/ -v
pytest --cov=src -v
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check tests/integration/ --fix
ruff format tests/integration/
mypy tests/integration/
```

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch.

**Commands:**
```bash
git add docs/issue_18_plan.md tests/integration/
git commit -m "test(api): implement end-to-end integration tests for M3 API endpoints (Issue #18)"
git push -u origin feature/issue-18-api-integration-tests
```

### Step 7: Merge into Develop

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-18-api-integration-tests
git branch -d feature/issue-18-api-integration-tests
git push origin develop
```

### Step 8: Finalize M3 — Merge Develop into Main

Conclude Milestone 3 (API Layer) by merging the tested codebase into `main`.

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
- [ ] Integration test suite set up in `tests/integration/`.
- [ ] End-to-end tests written using `httpx.AsyncClient` and in-memory SQLite fixture.
- [ ] Test coverage across the repository remains well above 80%.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch merged into `develop` and `develop` merged into `main`, completing Milestone M3.
