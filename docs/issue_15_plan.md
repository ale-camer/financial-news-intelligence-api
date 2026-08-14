# Issue #15 — POST /ingest/trigger (Manual Ingestion Trigger)

**Branch**: `feature/issue-15-ingest-trigger`  
**Milestone**: M3 (API Layer)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to expose an API endpoint (`POST /api/v1/ingest/trigger`) that allows triggering the ingestion and NLP pipelines on demand. This endpoint will orchestrate the fetching of news (M1), processing them through the NLP pipeline (M2), saving them to the database (M4 setup), and returning a summary of the operation. As requested, at the end of this issue, we will merge the progress from `develop` into the `main` branch to consolidate the core API functionality in production.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-15-ingest-trigger
```

### Step 2: Implement the Ingestion Endpoint

Create the API route module for ingestion tasks.

1. Create `src/api/routes/ingestion.py`.
2. Define a FastAPI `APIRouter`.
3. Create a `POST /trigger` endpoint.
   - Use `Depends(get_session)` for the database session.
   - Call `src.ingestion.orchestrator.run_ingestion` to fetch raw articles (you will pass dummy/test API keys or configure them via settings).
   - Convert the `RawArticle` models back into dictionaries because `process_batch` expects dictionaries.
   - Call `src.nlp.orchestrator.process_batch` to run sentiment analysis and NER.
   - Map the returned dictionaries to SQLAlchemy `Article` models and save them using the database session.
   - Handle unique constraints (e.g., catching `IntegrityError` to ignore duplicate links that already exist in the database).
   - Return a summary response (e.g., `{"status": "success", "articles_processed": N, "articles_saved": M}`).

### Step 3: Connect Router to Main App

Register the new router in the FastAPI app factory.

1. Open `src/api/main.py`.
2. Import the ingestion router (`from src.api.routes import ingestion`).
3. Include it in `create_app()`:
   ```python
   app.include_router(
       ingestion.router,
       prefix=settings.API_V1_STR + "/ingest",
       tags=["ingestion"]
   )
   ```

### Step 4: Write Unit Tests

Create unit tests to verify the trigger endpoint functions correctly.

1. Create `tests/unit/test_api_ingestion.py`.
2. Use `TestClient` and `patch` to mock the ingestion (`run_ingestion`) and NLP (`process_batch`) orchestrators to avoid making real HTTP/ML calls during testing.
3. Verify the endpoint returns `200 OK` and the correct processing summary payload.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_api_ingestion.py -v
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/api/ tests/unit/ --fix
ruff format src/api/ tests/unit/
mypy src/api/ tests/unit/
```

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch.

**Commands:**
```bash
git add docs/issue_15_plan.md src/api/ tests/unit/test_api_ingestion.py
git commit -m "feat(api): implement POST /ingest/trigger endpoint (Issue #15)"
git push -u origin feature/issue-15-ingest-trigger
```

### Step 7: Merge into Develop

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-15-ingest-trigger
git branch -d feature/issue-15-ingest-trigger
git push origin develop
```

### Step 8: Merge Develop into Main

Since Issues 13, 14, and 15 complete a highly functional core portion of the API Layer (M3), merge `develop` into `main` for stability.

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
- [ ] `POST /api/v1/ingest/trigger` endpoint correctly links the M1 (Ingestion) and M2 (NLP) pipelines.
- [ ] Validated NLP articles are saved to the database via SQLAlchemy.
- [ ] Duplicate articles are safely ignored (catching `IntegrityError`) without crashing the endpoint.
- [ ] Router is cleanly registered in `src/api/main.py`.
- [ ] Unit tests are implemented using mocks for both orchestrators.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
- [ ] `develop` branch is successfully merged into `main`.
