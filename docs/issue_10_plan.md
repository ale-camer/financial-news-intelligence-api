# Issue #10 — Deduplication & Text Preprocessing Utilities

**Branch**: `feature/issue-10-preprocessing`  
**Milestone**: M3 (NLP Processing)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to implement robust text preprocessing and deduplication utilities. Before passing financial news articles to our NLP pipelines (FinBERT and spaCy), we must clean the raw text (e.g., removing HTML tags, normalizing whitespaces) and ensure we are not processing duplicate articles (e.g., by generating content hashes like SHA-256 for exact match detection).

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-10-preprocessing
```

### Step 2: Implement Preprocessing Utilities

Create the module responsible for cleaning text and generating hashes.

1. Create the file `src/nlp/preprocessing.py`.
2. Import `re` and `hashlib`.
3. Create a function `def clean_text(text: str) -> str:`.
   - Remove HTML tags.
   - Normalize whitespace (replace multiple spaces/newlines with a single space).
   - Strip leading and trailing whitespace.
   - If the text is empty or missing, return an empty string.
4. Create a function `def generate_content_hash(text: str) -> str:`.
   - Take the cleaned text as input.
   - Generate and return a SHA-256 hex digest. This will be used later in the storage layer to detect and prevent exact duplicates from being processed.

### Step 3: Write Unit Tests

Ensure the preprocessing utilities behave correctly and consistently.

1. Create the file `tests/unit/test_preprocessing.py`.
2. Write tests to verify `clean_text`:
   - It properly removes HTML tags (e.g., `"<p>Hello <b>World</b></p>" -> "Hello World"`).
   - It normalizes spaces (e.g., `"  Too   many    spaces  " -> "Too many spaces"`).
   - It handles empty strings gracefully.
3. Write tests to verify `generate_content_hash`:
   - It generates the same hash for the exact same text.
   - It generates different hashes for different texts.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_preprocessing.py -v
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
git add docs/issue_10_plan.md src/nlp/preprocessing.py tests/unit/test_preprocessing.py
git commit -m "feat(nlp): implement text preprocessing and deduplication utils (Issue #10)"
git push -u origin feature/issue-10-preprocessing
```

### Step 6: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-10-preprocessing
git branch -d feature/issue-10-preprocessing
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `clean_text` correctly strips HTML and normalizes whitespace.
- [ ] `generate_content_hash` correctly computes a deterministic SHA-256 hash of a string.
- [ ] Unit tests cover both functions thoroughly, including edge cases.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
