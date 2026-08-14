# Issue #12 — Unit Tests & Coverage Stabilization

**Branch**: `feature/issue-12-test-coverage`  
**Milestone**: M2 (NLP Processing)  
**Type**: `test`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to stabilize the repository's test coverage. Currently, the global test coverage is around 59%, which causes our local `pytest` executions to fail due to the `--cov-fail-under=80` strict requirement set in `pyproject.toml`. We need to write the missing unit tests for the storage models, database configuration, schemas, and cover edge cases in the NLP sentiment module to surpass the 80% threshold.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-12-test-coverage
```

### Step 2: Implement Missing Tests

Create or update test files to cover the untested lines reported by pytest coverage.

1. **Storage Models (`tests/unit/test_models.py`)**:
   - Write tests to instantiate the database entities defined in `src/storage/models.py`.
2. **Database Config (`tests/unit/test_db.py`)**:
   - Test the database connection generator or session functions in `src/storage/db.py`. Use mocks (e.g., `unittest.mock.patch`) to avoid requiring a live database during unit testing.
3. **Article Schemas (`tests/unit/test_schemas.py`)**:
   - Instantiate Pydantic schemas defined in `src/schemas/article.py` and test validation errors for missing or invalid fields.
4. **Sentiment Edge Cases (`tests/unit/test_sentiment.py`)**:
   - The coverage report showed some lines in `src/nlp/sentiment.py` were missing. These correspond to the `try/except` blocks for model loading failures and the `sentiment_pipeline is None` fallback logic. Write tests that mock the pipeline to be `None` or raise an exception to cover these error-handling paths.

### Step 3: Verify Coverage

Ensure the global test coverage is now above 80%.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest -v
```
*(This command will automatically use the `addopts` from `pyproject.toml` which include the coverage report).*

### Step 4: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check tests/unit/ --fix
ruff format tests/unit/
mypy src/ tests/unit/
```

### Step 5: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add docs/issue_12_plan.md tests/unit/
git commit -m "test: improve unit test coverage to pass 80% threshold (Issue #12)"
git push -u origin feature/issue-12-test-coverage
```

### Step 6: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-12-test-coverage
git branch -d feature/issue-12-test-coverage
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] Global test coverage is >= 80% and `pytest` exits with code 0.
- [ ] Edge cases in `sentiment.py` are properly tested.
- [ ] Storage layer models, db configuration, and schemas have basic instantiation tests.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
