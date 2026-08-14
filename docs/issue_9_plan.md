# Issue #9 — spaCy Named Entity Recognition (Financial Entities)

**Branch**: `feature/issue-9-spacy-ner`  
**Milestone**: M3 (NLP Processing)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to implement a Named Entity Recognition (NER) module using the `spaCy` library. This module will process financial news text to extract relevant entities such as Organizations (ORG), Persons (PERSON), Geopolitical Entities (GPE), and Monetary values (MONEY). Extracting these entities will allow us to tag articles with the specific companies, executives, or regions they mention, enriching the metadata of our financial news pipeline.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-9-spacy-ner
```

### Step 2: Install Dependencies

Add the required NLP library `spacy` to the project and download the English language model.

**Commands:**
Add `"spacy>=3.7.0"` to the `dependencies` list in `pyproject.toml`, then run:
```bash
source .venv/bin/activate
pip install -e ".[dev]"
python -m spacy download en_core_web_sm
```

### Step 3: Implement the NER Module

Create the module responsible for entity extraction.

1. Create the file `src/nlp/ner.py`.
2. Import `spacy`.
3. Load the model at the module level: `nlp = spacy.load("en_core_web_sm")`. *(This prevents the model from reloading on every function call).*
4. Create a function `def extract_entities(text: str) -> list[dict[str, str]]:`.
5. The function should run the text through the spaCy pipeline and filter the extracted entities for relevant labels (e.g., `"ORG"`, `"PERSON"`, `"GPE"`, `"MONEY"`).
6. Return a list of dictionaries with the entity text and label. Example return: `[{"entity": "Apple", "label": "ORG"}, {"entity": "Tim Cook", "label": "PERSON"}]`. Ensure duplicate entities in the text are handled cleanly.
7. Handle edge cases: if the input string is empty or whitespace, return an empty list `[]`.

### Step 4: Write Unit Tests

Ensure the NER module extracts entities accurately.

1. Create the file `tests/unit/test_ner.py`.
2. Write tests to verify:
   - A text containing companies and people (e.g., "Tim Cook announced that Apple is opening a new office in London.") correctly identifies "Tim Cook" (PERSON), "Apple" (ORG), and "London" (GPE).
   - It handles financial text correctly (e.g., "$1.5 billion").
   - It handles empty strings gracefully without crashing.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_ner.py -v
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
git add pyproject.toml docs/issue_9_plan.md src/nlp/ner.py tests/unit/test_ner.py
git commit -m "feat(nlp): implement spacy named entity recognition (Issue #9)"
git push -u origin feature/issue-9-spacy-ner
```

### Step 7: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-9-spacy-ner
git branch -d feature/issue-9-spacy-ner
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `spacy` dependency is correctly managed in `pyproject.toml`.
- [ ] `en_core_web_sm` model is used for NER.
- [ ] `extract_entities` function correctly identifies relevant entities (ORG, PERSON, GPE, MONEY).
- [ ] Unit tests pass for standard entity extraction and edge cases.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
