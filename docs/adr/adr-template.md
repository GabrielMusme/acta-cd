# ADR Template

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Template

---

# Purpose

Provide the mandatory structure for new architectural decision records.

---

# Scope

Use this template for every new ADR created in the repository.

---

# Dependencies

- 00-project-design-handbook.md
- 12-mvp-execution-backlog.md
- 00-adr-index.md

---

# Definitions

- ADR ID: immutable identifier in DEC-XXX format.
- Source documents: normative documents that justify the decision.

---

# Requirements

- Include Context, Decision and Consequences.
- Reference the source documents explicitly.
- Do not rewrite an accepted ADR; create a new one if the decision changes.

---

# Design

## Metadata

- ADR ID: DEC-XXX
- Title: <decision title>
- Status: Proposed | Accepted | Superseded
- Date: YYYY-MM-DD
- Source documents:
  - 00-project-design-handbook.md
  - <other normative documents>

## Context

Describe the problem, constraints and why the decision is required now.

## Decision

State the chosen architectural decision in direct language.

## Consequences

- Positive consequences.
- Negative consequences.
- Deferred work or follow-up constraints.

---

# Diagrams

Add a diagram only if the decision cannot be understood clearly without one.

---

# Data Models

List any identifiers, fields or structural impacts introduced by the decision.

---

# Interfaces

List the interfaces, modules or boundaries affected by the decision.

---

# Error Handling

State what contradiction or implementation drift this ADR prevents.

---

# Implementation

List the immediate implementation implications and the first backlog tasks that depend on this decision.

---

# Open Questions

List unresolved questions that are not decided by this ADR.

---

# Future Improvements

Describe possible follow-up ADRs or refinements.

---

# Changelog

## 1.0.0

- Created ADR template.
