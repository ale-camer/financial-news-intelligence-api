# Issue #6 — PostgreSQL Schema (SQLAlchemy Models)

**Branch**: `feature/issue-6-sqlalchemy-models`  
**Milestone**: M2 (Storage & State Management)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

Kick off Milestone 2 by defining the database schema using SQLAlchemy 2.0 ORM. We need an `Article` model mapped to a PostgreSQL table to persist the raw and processed financial news data. This model will mirror the `ProcessedArticle` Pydantic schema, containing fields for both the original article content and the NLP outputs.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-6-sqlalchemy-models
```

**Validation:**
Ensure you are on the correct branch.
```bash
git branch --show-current
# Expected output: feature/issue-6-sqlalchemy-models
```

### Step 2: Install Dependencies

Add SQLAlchemy and the PostgreSQL driver to `pyproject.toml`.

**Commands:**
Add `"sqlalchemy>=2.0.0"` and `"psycopg2-binary>=2.9.0"` to the `dependencies` list in your `pyproject.toml`, then run:
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

**Validation:**
Ensure the packages are installed successfully.
```bash
python -c "import sqlalchemy; print(f'SQLAlchemy installed: {sqlalchemy.__version__}')"
# Expected output: SQLAlchemy installed: 2.x.x
```

### Step 3: Implement the SQLAlchemy Models

Define the declarative base and the `Article` table schema using modern SQLAlchemy 2.0 typing.

1. Create an `__init__.py` file inside `src/storage/` to make it a module.
2. Create the file `src/storage/models.py`.
3. Use SQLAlchemy 2.0 paradigms (`DeclarativeBase`, `Mapped`, `mapped_column`).
4. Define a `Base` class inheriting from `DeclarativeBase`.
5. Define an `Article` class with `__tablename__ = 'articles'`.
6. Add columns corresponding to our schema: `id` (Integer primary key), `title` (String), `link` (String, unique), `published_date` (String), `author` (String), `summary` (Text), `source` (String), `sentiment_score` (Float, nullable), `sentiment_label` (String, nullable), `entities` (JSON, nullable).

**Validation:**
Verify the code compiles and can instantiate an object.
```bash
python -c "from src.storage.models import Article; print(Article(title='Test').title)"
# Expected output: Test
```

### Step 4: Write Unit Tests

Ensure the ORM model acts as expected.

1. Create the file `tests/unit/test_models.py`.
2. Write a test case `test_article_model_instantiation` that creates an `Article` object with dummy data and asserts the attributes match.
3. Use a temporary in-memory SQLite database (`sqlite:///:memory:`) using SQLAlchemy's `create_engine` to run `Base.metadata.create_all(engine)` and test inserting/querying a row to ensure the schema compiles cleanly at the DB level.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_models.py -v
# Expected output: All tests passed.
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/storage/ tests/unit/ --fix
ruff format src/storage/ tests/unit/
mypy src/storage/ tests/unit/
```

**Validation:**
Ensure there are no remaining errors in the output of Ruff and MyPy. Clean output means success.

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add pyproject.toml docs/issue_6_plan.md src/storage/ tests/unit/test_models.py
git commit -m "feat(storage): implement sqlalchemy models for articles (Issue #6)"
git push -u origin feature/issue-6-sqlalchemy-models
```

**Validation:**
Check the Git status to ensure the working tree is clean.
```bash
git status
# Expected output: nothing to commit, working tree clean
```

### Step 7: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-6-sqlalchemy-models
git branch -d feature/issue-6-sqlalchemy-models
git push origin develop
```

**Validation:**
Ensure the branch is merged and no longer exists locally.
```bash
git branch
# Expected output: Should list 'develop' and 'main', but not 'feature/issue-6-sqlalchemy-models'.
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] SQLAlchemy and Psycopg2 dependencies are correctly managed.
- [ ] SQLAlchemy 2.0 `Article` model mirrors the business requirements and Pydantic schemas.
- [ ] Unit tests pass using an in-memory SQLite database to confirm schema correctness.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
