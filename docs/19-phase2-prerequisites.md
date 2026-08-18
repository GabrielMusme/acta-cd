# 19 - Phase 2 Prerequisites

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Active

---

# 1. Purpose

Define the local prerequisites and verification sequence before implementing Phase 2 persistence.

---

# 2. Dependencies

- 07-persistence-model.md
- 11-mvp-technology-stack.md
- 18-phase2-execution-backlog.md

---

# 3. Prerequisite Checklist

## 3.1 Runtime and Tooling

- [x] Python 3.12 target available.
- [x] uv environment and lock workflow available.
- [x] pytest and Ruff quality gate available.
- [x] SQLAlchemy 2.x added and locked.
- [x] Alembic added and locked.

## 3.2 PostgreSQL

- [x] PostgreSQL 16+ client installed (`psql`).
- [x] PostgreSQL 16+ readiness probe installed (`pg_isready`).
- [x] Local PostgreSQL service reachable.
- [x] Disposable test database can be created.
- [x] Test credentials provided through environment variables.

Verification procedure: [PostgreSQL 16+ local setup for Phase 2](phase2-postgresql-wsl.md).

Current verification status on 2026-08-17: P2-T01 verification passed with
PostgreSQL 16.15, environment-driven test credentials, and disposable database
creation/deletion.

## 3.3 Persistence Design

- [x] PostgreSQL is the normative database engine.
- [x] UUIDv7 policy is documented.
- [x] UTC timestamp policy is documented.
- [x] `deleted_at` soft-delete policy is documented.
- [x] Business Fact immutability policy is documented.
- [x] Concrete migration table design reviewed.
- [x] Repository boundary reviewed.

---

# 4. Verification Sequence

1. Install or provision PostgreSQL 16+ locally.
2. Run `pg_isready` against the configured host and port.
3. Create a disposable test database.
4. Add SQLAlchemy and Alembic dependencies.
5. Run the initial migration against the disposable database.
6. Execute persistence integration tests.
7. Drop and recreate the database to verify reproducibility.

---

# 5. Environment Contract

Required variables for future local integration tests:

- `ACTA_DATABASE_URL`
- `ACTA_TEST_DATABASE_URL`

Values SHALL remain outside versioned files.

---

# 6. Error Handling

- Missing PostgreSQL tools: block P2-T01 and database integration tests.
- Unreachable database: do not substitute SQLite because PostgreSQL behavior is normative.
- Missing credentials: fail configuration validation before opening a repository connection.

---

# 7. Changelog

## 1.1.0

- Implemented P2-T01 PostgreSQL WSL setup and verification workflow.
- Verified the local PostgreSQL service, connection health, and disposable database lifecycle.

## 1.0.0

- Created Phase 2 local prerequisite checklist and verification sequence.
- Recorded unavailable PostgreSQL client/readiness tools from the current environment.
