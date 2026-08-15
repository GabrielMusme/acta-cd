# ADR Index

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Active

---

# Purpose

Provide the registry for immutable architectural decision records used by this repository.

---

# Scope

This index lists approved ADR documents, their identifiers and their current status.

---

# Dependencies

- 00-project-design-handbook.md
- 10-implementation-plan.md
- 12-mvp-execution-backlog.md

---

# Definitions

- ADR: Architectural Decision Record.
- Immutable decision: a decision that is never edited in place; changes require a new ADR identifier.

---

# Requirements

- Every architectural decision SHALL receive an identifier.
- ADR identifiers SHALL use the DEC-XXX format.
- Decisions SHALL be immutable after approval.
- Each ADR SHALL reference its source documents.

---

# Design

## Registry

| ID | Status | Title | Source Documents |
| --- | --- | --- | --- |
| DEC-001 | Accepted | Modular monolith for MVP | 00, 10, 11, 12 |

## Workflow

1. Create a new ADR from the template.
2. Assign the next DEC identifier.
3. Record context, decision and consequences.
4. Reference the governing source documents.
5. If the decision changes, create a new ADR instead of rewriting the existing one.

---

# Diagrams

No diagrams are required for the ADR index.

---

# Data Models

The registry uses one row per ADR with identifier, status, title and source references.

---

# Interfaces

The index interfaces with ADR documents under this folder by linking their identifiers and titles.

---

# Error Handling

If an implementation depends on a decision that is not registered here, the implementation must stop until the ADR is created.

---

# Implementation

Initial registry created during P0-T04.

---

# Open Questions

- Should future ADRs include supersedes and superseded-by fields once decision volume grows?

---

# Future Improvements

- Add review dates if governance later requires periodic ADR audits.

---

# Changelog

## 1.0.0

- Created the initial ADR registry.
