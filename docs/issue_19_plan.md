# Issue #19 — MongoDB Repository: Article CRUD

**Branch**: `feature/issue-19-mongodb-repository`  
**Milestone**: M4 (Storage & Messaging)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to kick off **Milestone 4 (Storage & Messaging)** by implementing a MongoDB document repository pattern for article storage. This layer will provide asynchronous/synchronous CRUD operations (`save_article`, `get_article_by_id`, `list_articles`, `delete_article`) to persist enriched financial news documents in MongoDB, with indexing on key fields (`link`, `published_date`, `sentiment_label`).

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-19-mongodb-repository
```

### Step 2: Install Dependencies & Update Configuration

Add MongoDB client libraries and settings.

1. Update `pyproject.toml` to include runtime dependencies:
   - `pymongo>=4.6.0`
   - `motor>=3.3.0`
2. Update `src/api/config.py`:
   - Add `MONGODB_URL: str = "mongodb://localhost:27017"`
   - Add `MONGODB_DB_NAME: str = "financial_news"`

### Step 3: Implement MongoDB Client & Article Repository

Create the MongoDB database connection manager and repository class.

1. Create `src/storage/mongodb.py`:
   - Implement `get_mongo_client()` helper.
   - Define `ArticleRepository` class:
     - `save_article(article_data: dict[str, Any]) -> str`: Inserts a document and returns the string `ObjectId`.
     - `get_article_by_id(article_id: str) -> dict[str, Any] | None`: Retrieves a document by its `ObjectId` or custom ID.
     - `list_articles(filter_query: dict[str, Any] | None = None, skip: int = 0, limit: int = 10) -> list[dict[str, Any]]`: Queries articles with filtering and pagination.
     - `delete_article(article_id: str) -> bool`: Deletes a document by ID.
     - `create_indexes()`: Ensures unique index on `link` and single/compound indexes on `published_date` and `sentiment_label`.

### Step 4: Write Unit Tests

Ensure the repository CRUD operations function properly using mocks.

1. Create `tests/unit/test_mongodb_repository.py`.
2. Use `unittest.mock.MagicMock` / `mongomock` to mock MongoDB collection interactions.
3. Test each CRUD method (`save_article`, `get_article_by_id`, `list_articles`, `delete_article`).
4. Verify exception handling when document is not found or duplicate key errors occur.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_mongodb_repository.py -v
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/storage/ tests/unit/ --fix
ruff format src/storage/ tests/unit/
mypy src/storage/ tests/unit/
```

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch.

**Commands:**
```bash
git add docs/issue_19_plan.md pyproject.toml src/api/config.py src/storage/mongodb.py tests/unit/test_mongodb_repository.py
git commit -m "feat(storage): implement MongoDB ArticleRepository with CRUD operations (Issue #19)"
git push -u origin feature/issue-19-mongodb-repository
```

### Step 7: Merge into Develop

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-19-mongodb-repository
git branch -d feature/issue-19-mongodb-repository
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `pymongo` and `motor` dependencies added to `pyproject.toml`.
- [ ] MongoDB settings configured in `src/api/config.py`.
- [ ] `ArticleRepository` class implemented in `src/storage/mongodb.py` with full CRUD support.
- [ ] Indexes created for `link`, `published_date`, and `sentiment_label`.
- [ ] Unit tests for `ArticleRepository` pass with high coverage.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
