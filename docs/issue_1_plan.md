# Issue #1 — RSS Feed Ingestion Module

**Branch**: `feature/issue-1-rss-ingestion`  
**Milestone**: M1 (Ingestion & Scraping)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

Implement an RSS feed ingestion module to extract financial news from public sources (e.g., Yahoo Finance, CoinDesk, etc.), parse them, and normalize them into a common internal format. This module will serve as the first building block of the ingestion pipeline.

---

## Step-by-Step Execution Plan

Follow these steps sequentially. Run the validation commands after each step to ensure it was executed correctly.

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-1-rss-ingestion
```

**Validation:**
Ensure you are on the correct branch.
```bash
git branch --show-current
# Expected output: feature/issue-1-rss-ingestion
```

### Step 2: Install Dependencies

Add the necessary dependencies to `pyproject.toml` under `dependencies` (e.g., `feedparser` and `requests`), and install the project in editable mode.

**Commands:**
```bash
# Ensure your virtual environment is active
source .venv/bin/activate

# Install the project and its development dependencies
pip install -e ".[dev]"
```

**Validation:**
Check if the package is successfully installed.
```bash
python -c "import feedparser; print(feedparser.__version__)"
# Expected output: Should print the version number without any ModuleNotFoundError.
```

### Step 3: Implement the RSS Client

Create the ingestion module that fetches and parses the RSS feed.

1. Create the file `src/ingestion/rss_client.py`.
2. Implement an `RSSClient` class or a simple function `fetch_rss_feed(url: str) -> list[dict]`.
3. Extract key fields: `title`, `link`, `published_date`, `author`, `summary`.
4. Add basic error handling for network errors or malformed XML.

**Validation:**
Test the function manually using the Python REPL to ensure it works.
```bash
python -c "from src.ingestion.rss_client import fetch_rss_feed; print(fetch_rss_feed('https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL&region=US&lang=en-US')[:1])"
# Expected output: Should print at least one parsed news item dictionary.
```

### Step 4: Write Unit Tests

Ensure the code works as expected by mocking the RSS response.

1. Create the file `tests/unit/test_rss_client.py`.
2. Write a test case for a successful feed parsing using dummy XML or mocked dictionaries.
3. Write a test case for an invalid URL or malformed feed.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_rss_client.py -v
# Expected output: All tests passed (e.g., 2 passed in 0.05s).
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/ingestion/ tests/unit/ --fix
ruff format src/ingestion/ tests/unit/
mypy src/ingestion/ tests/unit/
```

**Validation:**
Ensure there are no remaining errors in the output of Ruff and MyPy. Clean output means success.

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add src/ingestion/rss_client.py tests/unit/test_rss_client.py
# If you updated pyproject.toml, add it as well: git add pyproject.toml
git commit -m "feat(ingestion): implement RSS feed ingestion module (Issue #1)"
git push -u origin feature/issue-1-rss-ingestion
```

**Validation:**
Check the Git status to ensure the working tree is clean.
```bash
git status
# Expected output: nothing to commit, working tree clean
```

### Step 7: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. *(Note: If you are using Pull Requests, you may perform the merge on GitHub and then pull `develop` locally).*

**Commands:**
```bash
git checkout develop
git merge feature/issue-1-rss-ingestion
git branch -d feature/issue-1-rss-ingestion
# Optional: push the merged develop branch to remote
git push origin develop
```

**Validation:**
Ensure the branch is merged and no longer exists locally.
```bash
git branch
# Expected output: Should list 'develop' and 'main', but not 'feature/issue-1-rss-ingestion'.
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `feedparser` dependency is successfully added and documented.
- [ ] `RSSClient` (or equivalent) successfully extracts `title`, `url`, `date`, and `summary` from an RSS feed.
- [ ] Unit tests pass, covering both success and error scenarios.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch `feature/issue-1-rss-ingestion` is successfully merged into `develop` and the local feature branch is deleted.
