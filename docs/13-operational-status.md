# 13 - Operational Status

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Active

---

## Depends On

- 10-implementation-plan.md
- 11-mvp-technology-stack.md
- 12-mvp-execution-backlog.md

---

# 1. Purpose

This file stores the current operational state so implementation can continue without relying on chat history.

---

# 2. Current Operational Baseline

- Development environment: VS Code connected to WSL Ubuntu 24.04.
- Target runtime: Ubuntu Server 24.04.
- Execution mode: implement and validate tasks in Linux-first workflow.
- Source of truth: repository documentation and versioned files.

---

# 3. Confirmed Decisions

- Use WSL Ubuntu 24.04 as the default development runtime.
- Keep code and execution inside WSL filesystem.
- Use Git as the primary synchronization mechanism.
- Keep manual file transfer tools as optional fallback, not default flow.

---

# 4. Next Planned Task

- Execute P1-T01 from 12-mvp-execution-backlog.md.
- Deliverables:
  - PersonName, EmailAddress, PostalAddress, TimeInterval, Duration, DateRange, VoteCount, ParticipantRole.

---

# 5. Local Environment Baseline

- Package manager and lock workflow: `uv sync --dev` updates the local environment and materializes `uv.lock`.
- Python runtime target: 3.12.x inside WSL Ubuntu 24.04.
- Editable local install: handled by `uv sync --dev` from the repository root.

## 5.1 Local Commands

- Install or refresh the environment: `uv sync --dev`
- Collect tests: `uv run pytest --collect-only`
- Run lint and format checks: `uv run ruff format --check . && uv run ruff check .`
- Run the single quality gate command: `./scripts/quality.sh`

---

# 6. Update Rule

When a relevant operational decision changes, update this file and append an entry to the changelog.

---

# 7. Changelog

## 1.4.0

- Completed P0-T06 with sample dataset policy and storage/naming conventions for data/meetings.
- Added metadata template and one policy-verification dataset template.
- Next planned task moves to P1-T01.

## 1.3.0

- Completed P0-T05 with conformance checklist template and task traceability matrix.
- Added contradiction protocol and one simulated closure record for checklist verification.
- Next planned task moves to P0-T06.

## 1.2.0

- Completed P0-T04 with ADR registry, ADR template and DEC-001 for the modular monolith MVP decision.
- Next planned task moves to P0-T05.

## 1.1.0

- Completed P0-T02 environment baseline with `pyproject.toml` and `uv` workflow.
- Completed P0-T03 quality gates with `ruff`, `pytest` and `scripts/quality.sh`.
- Next planned task moves to P0-T04.

## 1.0.0

- Created initial operational status snapshot after WSL setup confirmation.
