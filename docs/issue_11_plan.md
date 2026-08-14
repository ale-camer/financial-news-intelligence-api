# Issue #11 — NLP Pipeline Orchestrator (batch + async)

**Branch**: `feature/issue-11-nlp-orchestrator`  
**Milestone**: M3 (NLP Processing)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to create a unified orchestrator for the NLP module. This orchestrator will take raw article data, apply text preprocessing (Issue 10), and then pass the cleaned text through both the FinBERT sentiment analysis (Issue 8) and spaCy NER (Issue 9) pipelines. The orchestrator should provide a clean async interface for processing single articles or batches of articles efficiently.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-11-nlp-orchestrator
```

### Step 2: Implement the Orchestrator

Create the orchestrator module to unify the NLP tasks.

1. Create the file `src/nlp/orchestrator.py`.
2. Import the necessary functions:
   - `clean_text`, `generate_content_hash` from `src.nlp.preprocessing`
   - `analyze_sentiment` from `src.nlp.sentiment`
   - `extract_entities` from `src.nlp.ner`
   - `asyncio`
3. Create an async function `async def process_article(article_data: dict[str, str]) -> dict[str, any]:`.
   - The input `article_data` is a dictionary containing `text` (and optionally other metadata like `title`).
   - Call `clean_text` on the article's text.
   - Generate a content hash using `generate_content_hash`.
   - Call `analyze_sentiment` and `extract_entities`. You should wrap these in `asyncio.to_thread` since they are CPU-bound synchronous functions, preventing them from blocking the event loop.
   - Return a new dictionary that includes the original data plus `cleaned_text`, `content_hash`, `sentiment_label`, `sentiment_score`, and `entities`.
4. Create an async function `async def process_batch(articles: list[dict[str, str]]) -> list[dict[str, any]]:`.
   - Use `asyncio.gather` to concurrently process a batch of articles using `process_article`.

### Step 3: Write Unit Tests

Ensure the orchestrator successfully integrates all underlying NLP modules.

1. Create the file `tests/unit/test_nlp_orchestrator.py`.
2. Write tests (using `pytest.mark.asyncio`) to verify:
   - `process_article` correctly returns all expected enriched fields (hash, sentiment, entities).
   - `process_batch` successfully processes multiple articles concurrently.
   - The orchestrator handles edge cases (e.g., articles with missing or empty text).

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_nlp_orchestrator.py -v
```

### Step 4: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/nlp/ tests/unit/ --fix
ruff format src/nlp/ tests/unit/
mypy src/nlp/ tests/unit/
```

### Step 5: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add docs/issue_11_plan.md src/nlp/orchestrator.py tests/unit/test_nlp_orchestrator.py
git commit -m "feat(nlp): implement nlp pipeline orchestrator (Issue #11)"
git push -u origin feature/issue-11-nlp-orchestrator
```

### Step 6: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-11-nlp-orchestrator
git branch -d feature/issue-11-nlp-orchestrator
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `process_article` combines preprocessing, sentiment, and NER into a single result dictionary.
- [ ] `process_batch` correctly uses `asyncio` to process a list of articles.
- [ ] CPU-bound tasks (FinBERT, spaCy) are executed using `asyncio.to_thread` to prevent blocking the event loop.
- [ ] Unit tests cover both single and batch processing.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
