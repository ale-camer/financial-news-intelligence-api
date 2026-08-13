# Issue #3 — Web Scraping Module

**Branch**: `feature/issue-3-web-scraping`  
**Milestone**: M1 (Ingestion & Scraping)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

Implement a fallback web scraping module to extract article content when full text is not provided by RSS or NewsAPI. We will use `requests` and `BeautifulSoup` to parse HTML, extract the main article text, and return a clean string.

---

## Step-by-Step Execution Plan

Follow these steps sequentially. Run the validation commands after each step to ensure it was executed correctly.

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-3-web-scraping
```

**Validation:**
Ensure you are on the correct branch.
```bash
git branch --show-current
# Expected output: feature/issue-3-web-scraping
```

### Step 2: Install Dependencies

We need to add `beautifulsoup4` to our dependencies in `pyproject.toml` to parse HTML content.

**Commands:**
Add `"beautifulsoup4>=4.12.0"` to the `dependencies` list in your `pyproject.toml`, then run:
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

**Validation:**
Ensure the package is installed successfully.
```bash
python -c "import bs4; print('BeautifulSoup installed successfully')"
# Expected output: BeautifulSoup installed successfully
```

### Step 3: Implement the Web Scraper

Create the scraper module that fetches HTML and extracts text.

1. Create the file `src/ingestion/web_scraper.py`.
2. Implement a function `scrape_article_text(url: str) -> str`.
3. The function should use `requests` with a `User-Agent` header and a timeout.
4. Pass the HTML to `BeautifulSoup` using the built-in `"html.parser"`.
5. Extract the main text (e.g., by targeting `<p>` tags or specific generic article wrappers like `<article>`).
6. Add error handling for network timeouts or parsing issues, returning an empty string on failure.

**Validation:**
Test the function manually in the REPL with a sample article.
```bash
python -c "from src.ingestion.web_scraper import scrape_article_text; print(scrape_article_text('https://example.com')[:50])"
# Expected output: Some text extracted from the example page (e.g., "Example Domain").
```

### Step 4: Write Unit Tests

Ensure the code works as expected by mocking the HTML response.

1. Create the file `tests/unit/test_web_scraper.py`.
2. Write a test case for a successful response (mocking a `200 OK` HTML response with dummy `<p>` tags).
3. Write a test case for an API error or invalid URL.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_web_scraper.py -v
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
git add pyproject.toml src/ingestion/web_scraper.py tests/unit/test_web_scraper.py
git commit -m "feat(ingestion): implement web scraping module (Issue #3)"
git push -u origin feature/issue-3-web-scraping
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
git merge feature/issue-3-web-scraping
git branch -d feature/issue-3-web-scraping
git push origin develop
```

**Validation:**
Ensure the branch is merged and no longer exists locally.
```bash
git branch
# Expected output: Should list 'develop' and 'main', but not 'feature/issue-3-web-scraping'.
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `beautifulsoup4` dependency is successfully added and installed.
- [ ] `scrape_article_text` successfully extracts paragraph text from a given HTML URL.
- [ ] Unit tests pass, covering both success and error scenarios via mocks.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch `feature/issue-3-web-scraping` is successfully merged into `develop` and the local feature branch is deleted.
