# Issue #16 — GET /articles/{id}/sentiment (Sentiment Detail Endpoint)

**Branch**: `feature/issue-16-article-sentiment`  
**Milestone**: M3 (API Layer)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to expose an endpoint (`GET /api/v1/articles/{id}/sentiment`) that retrieves specific NLP insights (sentiment score, sentiment label, and extracted entities) for a single article stored in the database. If the article ID is not found, the endpoint must return a standard `404 Not Found` error.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-16-article-sentiment
```

### Step 2: Implement Response Schema

Define a focused response schema that only returns the relevant NLP insights.

1. Open `src/schemas/article.py`.
2. Create `ArticleSentimentResponse` inheriting from `BaseModel`.
3. Include fields:
   - `id: int`
   - `sentiment_score: float | None`
   - `sentiment_label: str | None`
   - `entities: list[dict[str, typing.Any]] | None`
4. Add `model_config = {"from_attributes": True}` for ORM compatibility.

### Step 3: Implement the Endpoint

Add the route to the existing articles router.

1. Open `src/api/routes/articles.py`.
2. Import `HTTPException` and `Path` from `fastapi`.
3. Import the new `ArticleSentimentResponse` schema.
4. Add the route:
   ```python
   @router.get("/{article_id}/sentiment", response_model=ArticleSentimentResponse)
   def get_article_sentiment(
       article_id: int = Path(..., title="The ID of the article"),
       session: Session = Depends(get_session),
   ) -> Any:
       # Query the database
       # Raise HTTPException(status_code=404, detail="Article not found") if not found
       # Return the article
   ```

### Step 4: Write Unit Tests

Ensure the endpoint works and handles missing articles properly.

1. Open `tests/unit/test_api_articles.py`.
2. Add a test function for a successful fetch:
   - Mock `session.query().filter().first()` to return a dummy article.
   - Assert `200 OK` and that the response matches the NLP fields.
3. Add a test function for `404 Not Found`:
   - Mock `session.query().filter().first()` to return `None`.
   - Assert `404` status code and error message.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_api_articles.py -v
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/schemas/ src/api/ tests/unit/ --fix
ruff format src/schemas/ src/api/ tests/unit/
mypy src/schemas/ src/api/ tests/unit/
```

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add docs/issue_16_plan.md src/schemas/article.py src/api/routes/articles.py tests/unit/test_api_articles.py
git commit -m "feat(api): implement GET /articles/{id}/sentiment endpoint (Issue #16)"
git push -u origin feature/issue-16-article-sentiment
```

### Step 7: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-16-article-sentiment
git branch -d feature/issue-16-article-sentiment
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `GET /api/v1/articles/{id}/sentiment` is implemented and functional.
- [ ] A `404 Not Found` response is raised if the ID does not exist.
- [ ] `ArticleSentimentResponse` schema successfully limits the returned fields.
- [ ] Unit tests cover both successful retrieval and `404` error handling.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
