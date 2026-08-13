# Issue #5 — Asynchronous Ingestion Orchestrator

**Branch**: `feature/issue-5-async-orchestrator`  
**Milestone**: M1 (Ingestion & Scraping)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

Create an asynchronous orchestrator that coordinates our ingestion modules (RSS and NewsAPI). By using `asyncio` and running our synchronous clients in separate threads (`asyncio.to_thread`), we can fetch data from multiple sources concurrently, greatly improving ingestion speed. The orchestrator will also be responsible for validating the incoming raw data and instantiating it as `RawArticle` Pydantic models.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-5-async-orchestrator
```

**Validation:**
Ensure you are on the correct branch.
```bash
git branch --show-current
# Expected output: feature/issue-5-async-orchestrator
```

### Step 2: Implement the Orchestrator

Create the module that manages concurrent ingestion.

1. Create the file `src/ingestion/orchestrator.py`.
2. Implement an asynchronous function `async def run_ingestion(newsapi_key: str, newsapi_query: str, rss_urls: list[str]) -> list[RawArticle]:`.
3. Inside the function, use `asyncio.to_thread` to wrap calls to `fetch_rss_feed` and `fetch_newsapi_feed` so they don't block the event loop.
4. Use `asyncio.gather` to execute all these tasks concurrently.
5. Iterate through the results, ignoring invalid ones, and convert the valid dictionaries into `RawArticle` objects using `RawArticle.model_validate()`. Use a `try/except ValidationError` block to skip corrupted items gracefully.
6. Return a flattened list of all successfully parsed `RawArticle` objects.

### Step 3: Write Unit Tests

Ensure the orchestrator fetches and combines data correctly.

1. Create the file `tests/unit/test_orchestrator.py`.
2. Use `@pytest.mark.asyncio` to write asynchronous tests.
3. Write a test case `test_run_ingestion_success` that mocks `fetch_rss_feed` and `fetch_newsapi_feed`, returning fake dictionaries.
4. Await `run_ingestion` and assert that it correctly combines the data into a list of `RawArticle` models.
5. Write a test case handling partial failures (e.g., one feed returns corrupted data that fails Pydantic validation) ensuring the orchestrator skips bad items but keeps the valid ones.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_orchestrator.py -v
# Expected output: All tests passed.
```

### Step 4: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/ingestion/ tests/unit/ --fix
ruff format src/ingestion/ tests/unit/
mypy src/ingestion/ tests/unit/
```

**Validation:**
Ensure there are no remaining errors in the output of Ruff and MyPy. Clean output means success.

### Step 5: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add docs/issue_5_plan.md src/ingestion/orchestrator.py tests/unit/test_orchestrator.py
git commit -m "feat(ingestion): implement async orchestrator and map to pydantic schemas (Issue #5)"
git push -u origin feature/issue-5-async-orchestrator
```

**Validation:**
Check the Git status to ensure the working tree is clean.
```bash
git status
# Expected output: nothing to commit, working tree clean
```

### Step 6: Merge and Milestone Release (Cleanup)

Merge the feature branch into `develop`, delete the local feature branch, and since this concludes Milestone 1, merge `develop` into `main` to cut the release. Finally, switch back to `develop` to continue future work.

**Commands:**
```bash
git checkout develop
git merge feature/issue-5-async-orchestrator
git branch -d feature/issue-5-async-orchestrator
git push origin develop
git checkout main
git merge develop
git push origin main
git checkout develop
```

**Validation:**
Ensure the branch is merged and no longer exists locally.
```bash
git branch
# Expected output: Should list 'develop' and 'main', but not 'feature/issue-5-async-orchestrator'.
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `orchestrator.py` uses `asyncio.gather` and `asyncio.to_thread` for concurrent network requests.
- [ ] Outputs are mapped strictly to `RawArticle` models, dropping corrupted dicts that fail validation.
- [ ] Unit tests cover success paths and partial failures (e.g., ValidationError handling).
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
