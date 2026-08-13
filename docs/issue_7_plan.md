# Issue #7 — PostgreSQL Database Service

**Branch**: `feature/issue-7-db-service`  
**Milestone**: M2 (Storage & State Management)  
**Type**: `feature`  
**Status**: 📋 Planned

---

## Objective

Now that our `Article` model is defined, we need a service to manage the connection to the PostgreSQL database. We will implement `src/storage/db.py` to create the SQLAlchemy engine, configure the session factory, and provide utility functions to initialize the database schema and safely yield active database sessions to our application.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-7-db-service
```

### Step 2: Implement the Database Service

Create the module responsible for database connections and sessions.

1. Create the file `src/storage/db.py`.
2. Import `create_engine` and `sessionmaker` from SQLAlchemy.
3. Import `os` to read `DATABASE_URL` from the environment variables (with a default fallback for local SQLite testing if missing, e.g. `sqlite:///local.db`).
4. Initialize the `engine = create_engine(...)` and `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`.
5. Write a function `init_db()` that imports `Base` from `src.storage.models` and calls `Base.metadata.create_all(bind=engine)`.
6. Write a generator function `get_session()` that yields a database session and ensures it is closed using a `try/finally` block.

### Step 3: Write Unit Tests

Ensure the connection manager creates sessions correctly.

1. Create the file `tests/unit/test_db.py`.
2. Write a test case `test_init_db` to verify that `Base.metadata.create_all` is called when initializing the database (use `unittest.mock.patch`).
3. Write a test case `test_get_session` to verify that the `get_session` generator yields a session and correctly calls `.close()` on the session when it finishes.

**Validation:**
Run the test suite using `pytest`.
```bash
pytest tests/unit/test_db.py -v
```

### Step 4: Code Quality & Linting

Format the code and check for static typing issues.

**Commands:**
```bash
ruff check src/storage/ tests/unit/ --fix
ruff format src/storage/ tests/unit/
mypy src/storage/ tests/unit/
```

### Step 5: Commit and Push

Stage the new files, commit the changes, and push the branch to the remote repository.

**Commands:**
```bash
git add docs/issue_7_plan.md src/storage/db.py tests/unit/test_db.py
git commit -m "feat(storage): implement database connection service (Issue #7)"
git push -u origin feature/issue-7-db-service
```

### Step 6: Merge and Cleanup

Merge the feature branch into `develop` and delete the local feature branch. 

**Commands:**
```bash
git checkout develop
git merge feature/issue-7-db-service
git branch -d feature/issue-7-db-service
git push origin develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] `db.py` successfully reads `DATABASE_URL` and creates an engine/session factory.
- [ ] `get_session()` properly yields a session and closes it in a `finally` block.
- [ ] Unit tests correctly validate the session creation and database initialization using mocks.
- [ ] Zero Ruff or MyPy errors.
- [ ] Branch is successfully merged into `develop`.
