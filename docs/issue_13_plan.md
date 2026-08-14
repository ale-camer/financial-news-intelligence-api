# Issue #13 — FastAPI App Factory & Config Management

**Branch**: `feature/issue-13-fastapi-factory`  
**Milestone**: M3 (API Layer)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to initialize Milestone 3 (API Layer) by creating the FastAPI application factory and setting up centralized configuration management using Pydantic Settings. We will also implement a basic `/health` endpoint to verify app initialization and setup unit tests using FastAPI's `TestClient`.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-13-fastapi-factory
```

### Step 2: Add Dependencies

Add `fastapi`, `uvicorn`, and `pydantic-settings` to `pyproject.toml` dependencies if not already present.

**Dependencies to verify in `pyproject.toml`**:
- `fastapi>=0.110.0`
- `uvicorn>=0.28.0`
- `pydantic-settings>=2.2.0`

### Step 3: Implement Config & App Factory

1. Create configuration module `src/api/config.py`:
   - Define a `Settings` class inheriting from `pydantic_settings.BaseSettings`.
   - Include environment variables: `PROJECT_NAME`, `DEBUG`, `API_V1_STR`, `DATABASE_URL`.
   - Instantiate a global `settings` object.
2. Create application factory `src/api/main.py`:
   - Define `create_app() -> FastAPI`.
   - Configure title, debug mode, and basic metadata from `settings`.
   - Include a `/health` endpoint returning `{"status": "ok", "app": settings.PROJECT_NAME}`.
   - Provide an entry point `app = create_app()`.

### Step 4: Write Unit Tests

Create unit tests to verify application instantiation and the `/health` endpoint.

1. Create `tests/unit/test_api_factory.py`.
2. Use `fastapi.testclient.TestClient` to test:
   - `GET /health` returns status code 200 and expected JSON payload.
   - App settings load correctly with defaults.

**Validation:**
```bash
pytest tests/unit/test_api_factory.py -v
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
git add docs/issue_13_plan.md pyproject.toml src/api/ tests/unit/test_api_factory.py
git commit -m "feat(api): implement fastapi app factory & config management (Issue #13)"
git push -u origin feature/issue-13-fastapi-factory
```

### Step 7: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-13-fastapi-factory
git branch -d feature/issue-13-fastapi-factory
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] Centralized configuration using `pydantic-settings` in `src/api/config.py`.
- [ ] Application factory `create_app()` defined in `src/api/main.py`.
- [ ] `/health` endpoint returns `200 OK` with status payload.
- [ ] Unit tests pass with `TestClient`.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
