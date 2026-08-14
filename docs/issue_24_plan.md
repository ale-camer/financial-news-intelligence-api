# Issue #24 — Dockerfile and Docker Compose (Production-Ready)

**Branch**: `feature/issue-24-docker`  
**Milestone**: M5 (Cloud Deploy & CI/CD)  
**Type**: `chore`  
**Status**: 📋 Planned

---

## Objective

The objective of this issue is to containerize the Financial News Intelligence API by creating a multi-stage, production-ready `Dockerfile` and updating `docker-compose.yml` to orchestrate all service dependencies (API, MongoDB, Redis, and Kafka) with health checks and non-root security.

---

## Step-by-Step Execution Plan

### Step 1: Git Branching Setup

Create and check out the feature branch for this issue from `develop`.

**Commands:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-24-docker
```

### Step 2: Create Multi-Stage Production Dockerfile

Create `infra/docker/Dockerfile` (and root `Dockerfile` symlink/reference) using Python slim base and security best practices.

1. Create `Dockerfile` with multi-stage build:
   - **Builder Stage**: Uses `python:3.14-slim`, installs build tools, creates virtualenv, and installs dependencies.
   - **Runner Stage**: Copies virtualenv and application code, creates a non-root `appuser`, exposes port 8000, and sets entrypoint:
     ```dockerfile
     CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
     ```

### Step 3: Update Docker Compose Configuration

Update `docker-compose.yml` to support local containerized execution.

1. Configure services:
   - `api`: Builds from `Dockerfile`, exposes port 8000, depends on `mongodb`, `redis`, and `kafka` with health checks.
   - `mongodb`: `mongo:latest` with volume persistence.
   - `redis`: `redis:7-alpine` with persistent volume.
   - `zookeeper` & `kafka`: `confluentinc/cp-kafka:latest` and `confluentinc/cp-zookeeper:latest`.

### Step 4: Write Tests / Verification

Verify Dockerfile syntax and container configuration without running full heavy builds if not required.

1. Create `tests/unit/test_docker_config.py`:
   - Validates existence and key directives of `Dockerfile` and `docker-compose.yml`.

### Step 5: Code Quality & Linting

Verify project linting and typing.

**Commands:**
```bash
ruff check src/ tests/ --fix
ruff format src/ tests/
mypy src/ tests/
```

### Step 6: Commit and Push

Stage files, commit, and push the branch.

**Commands:**
```bash
git add docs/issue_24_plan.md Dockerfile docker-compose.yml tests/unit/test_docker_config.py
git commit -m "chore(infra): add production-ready Dockerfile and docker-compose orchestration (Issue #24)"
git push -u origin feature/issue-24-docker
```

### Step 7: Merge into Develop

Merge feature branch into `develop` and clean up.

**Commands:**
```bash
git checkout develop
git merge feature/issue-24-docker
git branch -d feature/issue-24-docker
git push origin develop
```

### Step 8: Merge into Main

Promote updated code to `main`.

**Commands:**
```bash
git checkout main
git pull origin main
git merge develop
git push origin main
git checkout develop
```

---

## Acceptance Criteria

- [ ] All code and documentation are written in English.
- [ ] Production-ready multi-stage `Dockerfile` created.
- [ ] `docker-compose.yml` updated with API and infrastructure services.
- [ ] Configuration unit test in `tests/unit/test_docker_config.py` passes.
- [ ] Zero Ruff or MyPy errors.
- [ ] Feature branch merged into `develop` and `main`.
