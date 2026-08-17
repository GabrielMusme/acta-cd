# 18 - Phase 2 Execution Backlog

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

Translate the Phase 2 Persistence Foundation exit gate into executable tasks.

---

# 2. Scope

Phase 2 covers PostgreSQL persistence, mappings, migrations, repository behavior and persistence-specific integration tests.

It does not start processing, knowledge derivation or API implementation.

---

# 3. Dependencies

- 00-project-design-handbook.md
- 03-domain-model.md
- 04-business-facts.md
- 07-persistence-model.md
- 10-implementation-plan.md
- 11-mvp-technology-stack.md
- 13-operational-status.md
- 19-phase2-prerequisites.md

---

# 4. Working Rules

- Persistence adapters SHALL follow the domain model and SHALL NOT redefine it.
- Business Facts SHALL remain immutable and append-only in persistence.
- All persisted identifiers SHALL follow the UUIDv7 policy.
- All timestamps SHALL be UTC.
- Business records SHALL use `deleted_at` for soft deletion.
- Every task SHALL include repository or migration tests where applicable.

---

# 5. Phase 2 Tasks

## P2-T01 - Provision local PostgreSQL verification environment

Goal:

- provide a reproducible local PostgreSQL 16+ instance for integration tests.

Deliverables:

- documented installation or container workflow;
- database and test user configuration;
- connection health check.

Acceptance criteria:

- PostgreSQL 16+ is reachable locally;
- a clean test database can be created and dropped;
- credentials are supplied through environment variables, not committed files.

Verification:

- run `pg_isready`;
- connect with `psql`;
- create and drop a disposable test database.

## P2-T02 - Add persistence dependencies and configuration boundary

Goal:

- add SQLAlchemy 2.x and Alembic without coupling domain modules to persistence.

Deliverables:

- dependency updates and lockfile;
- infrastructure persistence settings;
- database URL configuration boundary.

Acceptance criteria:

- domain and business_facts packages import without database dependencies;
- invalid database configuration fails with a clear error;
- local configuration remains environment-driven.

Verification:

- import boundary test;
- configuration unit tests;
- clean `uv sync --dev`.

## P2-T03 - Define migration baseline

Goal:

- create the first reproducible Alembic migration for core domain tables.

Deliverables:

- Alembic environment;
- initial migration;
- migration execution instructions.

Acceptance criteria:

- migrations upgrade a clean database;
- migrations downgrade or recreate a clean database deterministically;
- names use snake_case and required `deleted_at` fields exist.

Verification:

- run upgrade on disposable database;
- inspect required tables and columns;
- rerun from clean state.

## P2-T04 - Implement domain persistence mappings

Goal:

- map Organization, Meeting, Person, Participant and core child entities to PostgreSQL.

Deliverables:

- SQLAlchemy mappings;
- explicit relationship constraints;
- UTC and UUIDv7 adapter policy.

Acceptance criteria:

- round-trip persistence preserves domain identity and relationships;
- soft delete does not physically remove records;
- persistence concerns remain outside domain entities.

Verification:

- repository integration tests;
- relationship and soft-delete tests.

## P2-T05 - Implement immutable Business Fact persistence

Goal:

- persist Business Facts with append-only write semantics and traceable references.

Deliverables:

- Business Fact mapping;
- fact reference mapping;
- immutable write policy.

Acceptance criteria:

- every fact requires one Meeting;
- every fact preserves category, occurred_at, payload and references;
- update and in-place overwrite attempts are rejected.

Verification:

- fact round-trip tests;
- append-only negative tests;
- reference integrity tests.

## P2-T06 - Build persistence integration test suite

Goal:

- create the Phase 2 evidence required by the exit gate.

Deliverables:

- PostgreSQL integration fixtures;
- round-trip test report;
- persistence gate checklist update.

Acceptance criteria:

- domain and fact round-trips pass;
- immutable fact policy passes;
- soft delete policy passes;
- migrations are reproducible.

Verification:

- run the complete persistence test subset;
- generate a Phase 2 persistence report.

---

# 6. Task Dependencies

- P2-T01 before P2-T02, P2-T03 and P2-T06.
- P2-T02 before P2-T03 and P2-T04.
- P2-T03 before P2-T04 and P2-T05.
- P2-T04 and P2-T05 before P2-T06.

---

# 7. Exit Gate

Phase 2 can close only when:

- domain and fact round-trip tests pass;
- immutable fact write policy is verified;
- soft delete policy is verified;
- local database creation and migration are reproducible.

---

# 8. Changelog

## 1.0.0

- Created Phase 2 Persistence Foundation backlog.
