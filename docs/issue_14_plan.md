# Issue #14 — GET /articles (List & Filter Endpoint)

**Branch**: `feature/issue-14-get-articles`  
**Milestone**: M3 (API Layer)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to implement our first core API endpoint: `GET /api/v1/articles`. This endpoint will query the database to retrieve processed articles and must support pagination (`skip`, `limit`) as well as basic filtering by `source` or `sentiment_label`.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-14-get-articles
```

### Step 2: Implement the Articles Router

Create the API route module to handle article endpoints.

1. Create `src/api/routes/__init__.py`.
2. Create `src/api/routes/articles.py`:
   - Import `APIRouter`, `Depends` from `fastapi`.
   - Import `Session` from `sqlalchemy.orm`.
   - Import `get_session` from `src.storage.db` and the `Article` model from `src.storage.models`.
   - Import the `ProcessedArticle` schema from `src.schemas.article` (or define a new response schema if needed).
   - Define a router: `router = APIRouter()`.
   - Define a `GET /` endpoint returning a list of articles.
   - Include query parameters: `skip: int = 0`, `limit: int = 10`, `source: str | None = None`, `sentiment_label: str | None = None`.
   - Build the SQLAlchemy query applying the filters dynamically, execute it, and return the mapped results.

### Step 3: Connect Router to Main App

Update the FastAPI application factory to include the new router.

1. Open `src/api/main.py`.
2. Import the newly created router: `from src.api.routes import articles`.
3. Inside `create_app()`, register the router:
   ```python
   app.include_router(
       articles.router,
       prefix=settings.API_V1_STR + "/articles",
       tags=["articles"]
   )
   ```

### Step 4: Write Unit Tests

Ensure the new endpoint handles querying and filtering correctly without needing a live database.

1. Create `tests/unit/test_api_articles.py`.
2. Use `fastapi.testclient.TestClient`.
3. Use FastAPI's `app.dependency_overrides` to mock the `get_session` dependency.
4. Write tests for:
   - Returning a standard paginated list.
   - Returning a filtered list by `sentiment_label`.
   - Returning an empty list if no results match.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_api_articles.py -v
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

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add docs/issue_14_plan.md src/api/ tests/unit/test_api_articles.py
git commit -m "feat(api): implement GET /articles endpoint with filtering (Issue #14)"
git push -u origin feature/issue-14-get-articles
```

### Step 7: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-14-get-articles
git branch -d feature/issue-14-get-articles
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `GET /api/v1/articles` correctly queries the database using SQLAlchemy.
- [ ] Pagination (`skip`, `limit`) and filters (`source`, `sentiment_label`) work.
- [ ] Router is cleanly registered in `src/api/main.py`.
- [ ] Unit tests are implemented using `dependency_overrides` for the DB session.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
