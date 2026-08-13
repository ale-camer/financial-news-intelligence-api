# Issue #2 — NewsAPI Integration Module

**Branch**: `feature/issue-2-newsapi-integration`  
**Milestone**: M1 (Ingestion & Scraping)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

Implement a module to extract financial news using the [NewsAPI](https://newsapi.org/) REST service. This module will fetch the news, parse the JSON response, and normalize it into the same common internal format (dictionary with `title`, `link`, `published_date`, `author`, and `summary`) used by the RSS client. It will rely on a `NEWSAPI_KEY` environment variable.

---

## Step-by-Step Execution Plan

Follow these steps sequentially. Run the validation commands after each step to ensure it was executed correctly.

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-2-newsapi-integration
```

**Validation:**
Ensure you are on the correct branch.
```bash
git branch --show-current
# Expected output: feature/issue-2-newsapi-integration
```

### Step 2: Install Configuration Dependencies

We will use `requests` (already installed) to make the API calls, but we should install `python-dotenv` to securely load the API key from a `.env` file during local development.

**Commands:**
Add `"python-dotenv>=1.0.1"` to the `dependencies` list in your `pyproject.toml`, then run:
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

**Validation:**
Ensure the environment package is installed successfully.
```bash
python -c "import dotenv; print('dotenv loaded successfully')"
# Expected output: dotenv loaded successfully
```

### Step 3: Implement the NewsAPI Client

Create the ingestion module that fetches and parses news from NewsAPI.

1. Ensure your `.env` file has a valid `NEWSAPI_KEY=your_api_key_here`. (You can get a free dev key at newsapi.org).
2. Create the file `src/ingestion/newsapi_client.py`.
3. Implement a function `fetch_newsapi_feed(query: str, api_key: str) -> list[dict]`.
4. Parse the JSON response. The endpoint to use is usually `https://newsapi.org/v2/everything`.
5. Normalize the output: map `title`, `url` (to `link`), `publishedAt` (to `published_date`), `author`, and `description` (to `summary`).
6. Add error handling (e.g., handling 401 Unauthorized or network timeouts).

**Validation:**
Test the function manually in the REPL.
```bash
# Assuming you have loaded your env var or pass it explicitly:
python -c "import os; from src.ingestion.newsapi_client import fetch_newsapi_feed; print(fetch_newsapi_feed('finance', os.getenv('NEWSAPI_KEY', 'fake_key'))[:1])"
# Expected output: A list with at least one dictionary, or an empty list if using a fake key.
```

### Step 4: Write Unit Tests

Ensure the code works as expected by mocking the API JSON response.

1. Create the file `tests/unit/test_newsapi_client.py`.
2. Write a test case for a successful response (mocking a `200 OK` JSON response).
3. Write a test case for an API error (e.g., `401 Unauthorized` or network exception).

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_newsapi_client.py -v
# Expected output: All tests passed.
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
git add pyproject.toml src/ingestion/newsapi_client.py tests/unit/test_newsapi_client.py
git commit -m "feat(ingestion): implement NewsAPI integration module (Issue #2)"
git push -u origin feature/issue-2-newsapi-integration
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
git merge feature/issue-2-newsapi-integration
git branch -d feature/issue-2-newsapi-integration
git push origin develop
```

**Validation:**
Ensure the branch is merged and no longer exists locally.
```bash
git branch
# Expected output: Should list 'develop' and 'main', but not 'feature/issue-2-newsapi-integration'.
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `python-dotenv` dependency is successfully added and installed.
- [ ] `fetch_newsapi_feed` successfully maps the API response to the standard dictionary format.
- [ ] Secrets (like `NEWSAPI_KEY`) are NOT hardcoded, but read from the environment.
- [ ] Unit tests pass, covering both success and error scenarios via mocks.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch `feature/issue-2-newsapi-integration` is successfully merged into `develop` and the local feature branch is deleted.
