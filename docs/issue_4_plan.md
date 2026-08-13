# Issue #4 — Pydantic Schemas for Raw & Processed Articles

**Branch**: `feature/issue-4-pydantic-schemas`  
**Milestone**: M1 (Ingestion & Scraping)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

Create strictly typed data models using Pydantic V2 to represent financial news articles throughout the application. We need a `RawArticle` schema for newly ingested data and a `ProcessedArticle` schema (which inherits from `RawArticle`) to hold NLP outputs like sentiment and named entities. This ensures data consistency across the ingestion, NLP, and API pipelines.

---

## Step-by-Step Execution Plan

Follow these steps sequentially. Run the validation commands after each step to ensure it was executed correctly.

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-4-pydantic-schemas
```

**Validation:**
Ensure you are on the correct branch.
```bash
git branch --show-current
# Expected output: feature/issue-4-pydantic-schemas
```

### Step 2: Install Dependencies

We need to add `pydantic` to our project dependencies to handle data validation.

**Commands:**
Add `"pydantic>=2.0.0"` to the `dependencies` list in your `pyproject.toml`, then run:
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

**Validation:**
Ensure the package is installed successfully.
```bash
python -c "import pydantic; print(f'Pydantic installed: {pydantic.__version__}')"
# Expected output: Pydantic installed: 2.x.x
```

### Step 3: Implement the Schemas

Create the shared schema module.

1. Create a new directory `src/schemas/` and add an empty `__init__.py` file inside it.
2. Create the file `src/schemas/article.py`.
3. Define a `RawArticle` model inheriting from `pydantic.BaseModel`. It should include: `title` (str), `link` (str, or HttpUrl), `published_date` (str), `author` (str), `summary` (str), and `source` (str, e.g., 'rss' or 'newsapi').
4. Define a `ProcessedArticle` model inheriting from `RawArticle`. It should add fields like `sentiment_score` (float), `sentiment_label` (str), and `entities` (list of strings or dicts).

**Validation:**
Test the schema manually in the REPL.
```bash
python -c "from src.schemas.article import RawArticle; article = RawArticle(title='Test', link='http://test.com', published_date='2026-08-13', author='John', summary='Summary', source='rss'); print(article.title)"
# Expected output: Test
```

### Step 4: Write Unit Tests

Ensure the models validate correctly and reject bad data.

1. Create the file `tests/unit/test_schemas.py`.
2. Write a test case where a valid dictionary is successfully parsed into a `RawArticle`.
3. Write a test case that expects a `pydantic.ValidationError` when required fields are missing.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_schemas.py -v
# Expected output: All tests passed.
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/schemas/ tests/unit/ --fix
ruff format src/schemas/ tests/unit/
mypy src/schemas/ tests/unit/
```

**Validation:**
Ensure there are no remaining errors in the output of Ruff and MyPy. Clean output means success.

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add pyproject.toml src/schemas/ tests/unit/test_schemas.py
git commit -m "feat(schemas): implement pydantic models for articles (Issue #4)"
git push -u origin feature/issue-4-pydantic-schemas
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
git merge feature/issue-4-pydantic-schemas
git branch -d feature/issue-4-pydantic-schemas
git push origin develop
```

**Validation:**
Ensure the branch is merged and no longer exists locally.
```bash
git branch
# Expected output: Should list 'develop' and 'main', but not 'feature/issue-4-pydantic-schemas'.
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `pydantic` dependency is successfully added and installed.
- [ ] `RawArticle` and `ProcessedArticle` schemas are correctly defined.
- [ ] Unit tests pass, verifying both successful parsing and `ValidationError` on bad data.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch `feature/issue-4-pydantic-schemas` is successfully merged into `develop` and the local feature branch is deleted.
