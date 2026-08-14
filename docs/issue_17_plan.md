# Issue #17 — API Middleware: Logging, Process Time & Global Error Handling

**Branch**: `feature/issue-17-middleware`  
**Milestone**: M3 (API Layer)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to make our FastAPI application production-ready by implementing essential middleware and exception handling:
1. **Process Time & Logging Middleware**: Log incoming HTTP requests and measure execution time, attaching an `X-Process-Time` response header.
2. **Global Error Handler**: Intercept unhandled internal server exceptions and return a structured JSON response instead of default 500 HTML/raw tracebacks.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-17-middleware
```

### Step 2: Implement Middleware and Exception Handlers

Create dedicated modules for middleware and error handling.

1. Create `src/api/middleware.py`:
   - Define an async HTTP middleware `add_process_time_header(request: Request, call_next)` that measures execution time using `time.perf_counter()`.
   - Log request details (method, path, status code, process time).
   - Add the `X-Process-Time` header to the response.
2. Create `src/api/exceptions.py`:
   - Define a custom exception handler `global_exception_handler(request: Request, exc: Exception)` returning a structured `JSONResponse` with status code 500 and payload `{"detail": "Internal Server Error", "error_code": "INTERNAL_SERVER_ERROR"}`.

### Step 3: Register in App Factory

Update `src/api/main.py` to register the middleware and exception handler.

1. Open `src/api/main.py`.
2. Import `add_process_time_header` from `src.api.middleware`.
3. Import `global_exception_handler` from `src.api.exceptions`.
4. Register the middleware in `create_app()` using `app.middleware("http")(add_process_time_header)`.
5. Register the exception handler using `app.add_exception_handler(Exception, global_exception_handler)`.

### Step 4: Write Unit Tests

Ensure the middleware and error handling behave as expected.

1. Create `tests/unit/test_api_middleware.py`.
2. Test that any API response (e.g. `GET /health`) includes the `X-Process-Time` header.
3. Test that an unhandled exception in a route returns a structured `500` JSON payload rather than a default error page.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_api_middleware.py -v
```

### Step 5: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/api/ tests/unit/ --fix
ruff format src/api/ tests/unit/
mypy src/api/ tests/unit/
```

### Step 6: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add docs/issue_17_plan.md src/api/middleware.py src/api/exceptions.py src/api/main.py tests/unit/test_api_middleware.py
git commit -m "feat(api): add process time middleware and global exception handler (Issue #17)"
git push -u origin feature/issue-17-middleware
```

### Step 7: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-17-middleware
git branch -d feature/issue-17-middleware
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `X-Process-Time` header is added to all HTTP responses.
- [ ] Incoming requests are logged with timing information.
- [ ] Global exception handler catches unhandled exceptions and returns a clean 500 JSON response.
- [ ] Middleware and exception handlers are registered in `src/api/main.py`.
- [ ] Unit tests pass for both middleware and exception handling.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
