# DEC-001 - Modular Monolith for MVP

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Accepted

---

# Purpose

Record the architectural decision that defines the MVP deployment and package organization baseline.

---

# Scope

This ADR governs the MVP implementation shape for the application runtime and internal module boundaries.

---

# Dependencies

- 00-project-design-handbook.md
- 09-project-structure.md
- 10-implementation-plan.md
- 11-mvp-technology-stack.md
- 12-mvp-execution-backlog.md

---

# Definitions

- Modular monolith: a single deployable service that preserves explicit internal boundaries between domains and infrastructure.
- MVP: the minimum end-to-end implementation approved for the first delivery slice.

---

# Requirements

- Preserve domain separation required by ARCH-008 and ARCH-009.
- Keep the MVP operationally simple for a one-person implementation flow.
- Avoid introducing multi-service deployment complexity before Phase 5 hardening.

---

# Design

## Metadata

- ADR ID: DEC-001
- Date: 2026-08-15
- Source documents:
  - 00-project-design-handbook.md
  - 09-project-structure.md
  - 10-implementation-plan.md
  - 11-mvp-technology-stack.md
  - 12-mvp-execution-backlog.md

## Context

Phase 0 requires an execution baseline that can be implemented and validated locally on WSL Ubuntu 24.04 with limited operational overhead. The implementation plan defines a one-person delivery model and requires explicit internal boundaries before coding expands into persistence, processing and APIs. The MVP technology stack already resolved the architecture question in favor of a modular monolith, but the decision was not yet captured as an immutable ADR.

## Decision

The MVP SHALL be implemented as a modular monolith: one deployable Python service with explicit package boundaries for app, domain, business facts, knowledge, processing, infrastructure and shared concerns.

## Consequences

- Positive: reduces deployment and debugging complexity during Phases 0 to 4.
- Positive: keeps the upgrade path open for later process separation without collapsing domain boundaries.
- Negative: runtime isolation between API and background processing is deferred.
- Negative: scalability decisions for independent services remain postponed until operational evidence exists.
- Follow-up: future changes to deployment topology require a new ADR instead of modifying this decision.

---

# Diagrams

No additional diagram is required because the module boundaries are already represented in the approved project structure documents.

---

# Data Models

This decision does not introduce new persisted data structures.

---

# Interfaces

Affected interfaces:

- Internal application service boundaries between app and domain packages.
- Processing orchestration interfaces inside the same deployable runtime.
- Persistence and export adapters loaded within the monolith.

---

# Error Handling

This ADR prevents undocumented drift toward premature microservices or ad hoc coupling across package boundaries.

---

# Implementation

- Phase 0 uses a single Python project and toolchain.
- Phase 1 and later tasks must preserve package boundaries instead of introducing cross-layer shortcuts.
- Any future runtime split must reference this ADR and add a superseding decision.

---

# Open Questions

- What operational thresholds would justify splitting workers or API runtime into separate deployables later?

---

# Future Improvements

- Add a superseding ADR if production hardening requires independent worker deployment.

---

# Changelog

## 1.0.0

- Created DEC-001 for the modular monolith MVP baseline.
