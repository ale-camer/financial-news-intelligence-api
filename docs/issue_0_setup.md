# Issue #0 — Day 0: Project Setup & Scaffolding

**Branch**: `feature/day-0-setup`  
**Milestone**: Pre-M1 (Repository Initialization)  
**Type**: `chore`  
**Status**: 🔄 In Progress

---

## Objective

Bootstrap the project repository with the foundational structure, configuration files, and documentation. No business logic is written in this issue. The goal is a clean, well-organized starting point from which all future issues will be developed.

---

## Checklist

### Git & Branching

- [x] `git init` — repository initialized
- [x] Initial empty commit on `main`
- [x] `develop` branch created from `main`
- [x] `feature/day-0-setup` branch created from `develop`
- [ ] `feature/day-0-setup` merged to `develop` via PR
- [ ] GitHub remote repository created (`gh repo create`)

### Virtual Environment

- [x] `.venv` created with `python3 -m venv .venv`
- [x] Python version verified: **3.14.5**
- [x] `.venv/` added to `.gitignore`

### Configuration Files

- [x] `.gitignore` — Python, IDE, Docker, Terraform, GCP patterns
- [x] `.env.example` — all required environment variables documented
- [x] `pyproject.toml` — project metadata + Ruff, MyPy, pytest config

### Directory Structure

- [x] `src/` — application source root
- [x] `src/api/` — FastAPI routes and app factory (M3)
- [x] `src/ingestion/` — RSS, NewsAPI, scraping modules (M1)
- [x] `src/nlp/` — NLP pipeline, sentiment, NER (M2)
- [x] `src/storage/` — MongoDB + Redis repositories (M4)
- [x] `src/messaging/` — Kafka producer/consumer (M4)
- [x] `tests/unit/` — isolated unit tests
- [x] `tests/integration/` — integration and API tests
- [x] `infra/terraform/` — GCP Terraform configurations (M5)
- [x] `infra/docker/` — Dockerfile(s) (M5)
- [x] `.github/workflows/` — CI/CD pipeline definitions (M5)

### Documentation

- [x] `README.md` — architecture diagram (Mermaid), tech stack, roadmap
- [x] `docs/issue_0_setup.md` — this file

### Infrastructure Skeleton

- [x] `docker-compose.yml` — services declared (api, mongodb, redis, zookeeper, kafka) without business configuration

### GitHub Setup

- [ ] Repository created as public: `financial-news-intelligence-api`
- [ ] Milestones created (5):
  - [ ] M1 — Ingestion & Scraping
  - [ ] M2 — NLP Processing
  - [ ] M3 — API Layer
  - [ ] M4 — Storage & Messaging
  - [ ] M5 — Cloud Deploy & CI/CD
- [ ] Issues created (target: 24 atomic issues)
- [ ] Labels configured (`feature`, `fix`, `chore`, `docs`, `test`)

---

## Issue Map (24 Atomic Issues)

### M1 — Ingestion & Scraping

| # | Title | Type |
|---|---|---|
| 1 | RSS Feed Ingestion Module | `feature` |
| 2 | NewsAPI Integration Module | `feature` |
| 3 | Web Scraping Module (requests + BeautifulSoup) | `feature` |
| 4 | Pydantic Schemas for Raw & Processed Articles | `feature` |
| 5 | Unit Tests — Ingestion Layer | `test` |

### M2 — NLP Processing

| # | Title | Type |
|---|---|---|
| 6 | FinBERT Sentiment Classification Pipeline | `feature` |
| 7 | spaCy Named Entity Recognition (Financial Entities) | `feature` |
| 8 | Deduplication & Text Preprocessing Utilities | `feature` |
| 9 | NLP Pipeline Orchestrator (batch + async) | `feature` |
| 10 | Unit Tests — NLP Layer | `test` |

### M3 — API Layer

| # | Title | Type |
|---|---|---|
| 11 | FastAPI App Factory & Config Management | `feature` |
| 12 | `GET /articles` — List & Filter Endpoint | `feature` |
| 13 | `POST /ingest/trigger` — Manual Ingestion Trigger | `feature` |
| 14 | `GET /articles/{id}/sentiment` — Sentiment Detail | `feature` |
| 15 | Middleware: Rate Limiting, Logging, Error Handlers | `feature` |
| 16 | Integration Tests — API Endpoints (httpx) | `test` |

### M4 — Storage & Messaging

| # | Title | Type |
|---|---|---|
| 17 | MongoDB Repository — Article CRUD | `feature` |
| 18 | Redis Cache Layer — Recent Results TTL | `feature` |
| 19 | Kafka Producer — `news.processed` Event Publishing | `feature` |
| 20 | Kafka Consumer — `market.events.raw` (P-03 integration) | `feature` |
| 21 | Integration Tests — Storage & Kafka | `test` |

### M5 — Cloud Deploy & CI/CD

| # | Title | Type |
|---|---|---|
| 22 | Dockerfile + Docker Compose (production-ready) | `chore` |
| 23 | Terraform — GCP Cloud Run + GCS Resources | `chore` |
| 24 | GitHub Actions CI/CD Pipeline (lint → test → build → deploy) | `chore` |

---

## Notes

- All business logic, imports, and dependencies will be introduced per-issue in their respective feature branches.
- The `docker-compose.yml` services use Docker `profiles` to allow selective startup during development.
- `pyproject.toml` `dependencies = []` is intentional — runtime deps will be added starting in M1.

---

## Acceptance Criteria

- All checkboxes above are ticked ✅
- `feature/day-0-setup` is merged to `develop` via a clean PR
- CI/CD pipeline placeholder exists in `.github/workflows/`
- Repository is publicly accessible on GitHub
