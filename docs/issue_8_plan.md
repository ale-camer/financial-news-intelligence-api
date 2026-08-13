# Issue #8 — FinBERT Sentiment Classification Pipeline

**Branch**: `feature/issue-8-finbert-sentiment`  
**Milestone**: M3 (NLP Processing)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

We are now kicking off the NLP phase! The objective of this issue is to implement a sentiment analysis pipeline using the Hugging Face `transformers` library, specifically utilizing the `ProsusAI/finbert` model (which is pre-trained on financial text). This module will take the raw text/summary of an article and classify its sentiment as Positive, Negative, or Neutral, returning both the label and the confidence score.

*(Note: We adapted the roadmap slightly since we implemented the PostgreSQL storage layer in issues 6 and 7).*

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-8-finbert-sentiment
```

### Step 2: Install Dependencies

Add the required machine learning libraries to `pyproject.toml`.

**Commands:**
Add `"transformers>=4.30.0"` and `"torch>=2.0.0"` to the `dependencies` list in `pyproject.toml`, then run:
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

### Step 3: Implement the FinBERT Pipeline

Create the module responsible for running the sentiment analysis.

1. Create the file `src/nlp/sentiment.py`.
2. Import `pipeline` from `transformers`.
3. Initialize the model at the module level: `sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")`. *(This prevents the ~400MB model from reloading on every function call).*
4. Create a function `def analyze_sentiment(text: str) -> tuple[str, float]:`.
5. The function should run the text through the pipeline and return a tuple of `(sentiment_label, score)` (e.g. `("POSITIVE", 0.95)`). 
6. Handle edge cases: if the input string is empty or whitespace, return `("NEUTRAL", 0.0)`.

### Step 4: Write Unit Tests

Ensure the NLP pipeline classifies financial text accurately without breaking.

1. Create the file `tests/unit/test_sentiment.py`.
2. Write tests to verify:
   - A clearly positive financial text (e.g., "Company revenue skyrocketed by 200%") returns a "positive" label.
   - A clearly negative financial text (e.g., "Stocks plummeted amid bankruptcy fears") returns a "negative" label.
   - It handles empty strings gracefully.
3. *Note: Running this test the very first time will download the FinBERT model to your local HuggingFace cache.*

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_sentiment.py -v
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/nlp/ tests/unit/ --fix
ruff format src/nlp/ tests/unit/
mypy src/nlp/ tests/unit/
```

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add pyproject.toml docs/issue_8_plan.md src/nlp/sentiment.py tests/unit/test_sentiment.py
git commit -m "feat(nlp): implement finbert sentiment analysis pipeline (Issue #8)"
git push -u origin feature/issue-8-finbert-sentiment
```

### Step 7: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-8-finbert-sentiment
git branch -d feature/issue-8-finbert-sentiment
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `transformers` and `torch` dependencies are correctly managed.
- [ ] `analyze_sentiment` correctly infers sentiment using `ProsusAI/finbert`.
- [ ] Unit tests pass for positive, negative, and edge cases.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
