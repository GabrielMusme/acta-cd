# 15 - Task Traceability Matrix

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Active

---

# 1. Purpose

Link backlog tasks to source documents and governing rule IDs, so each implementation slice is auditable.

---

# 2. Scope

This matrix starts with completed Phase 0 tasks and is expanded as new tasks are implemented.

---

# 3. Dependencies

- 00-project-design-handbook.md
- 10-implementation-plan.md
- 11-mvp-technology-stack.md
- 12-mvp-execution-backlog.md
- 14-conformance-checklist.md

---

# 4. Definitions

- Rule ID: identifier of a mandatory requirement, principle or decision.
- Task mapping: explicit relation between one task and one or more rule IDs.

---

# 5. Design

## 5.1 Mapping Table

| Task ID | Task Title | Source Documents | Rule IDs | Evidence |
| --- | --- | --- | --- | --- |
| P0-T01 | Create project skeleton | 09, 10, 12 | DOC-001, ARCH-008, ARCH-009 | src/, tests/, scripts/, data/meetings/ base structure and smoke import test |
| P0-T02 | Initialize Python environment and toolchain | 10, 11, 12 | DOC-001, DOC-005 | pyproject.toml, uv.lock, documented local commands |
| P0-T03 | Configure quality gates | 10, 11, 12 | DOC-001, DOC-005 | ruff and pytest baseline plus scripts/quality.sh single command |
| P0-T04 | Create ADR registry and templates | 00, 10, 11, 12 | DOC-002, DOC-005 | docs/adr/00-adr-index.md, docs/adr/adr-template.md, DEC-001 |
| P0-T05 | Create conformance and traceability checklist | 00, 10, 12 | DOC-001, DOC-004, DOC-005, DOC-009 | docs/14-conformance-checklist.md and docs/15-task-traceability-matrix.md |
| P0-T06 | Define sample data policy | 00, 10, 12 | ARCH-001, ARCH-002, DOC-001, DOC-005 | docs/16-sample-data-policy.md, data/meetings/README.md, data/meetings/metadata-template.yaml |
| P1-T01 | Implement domain value objects | 03, 12 | DM-REQ-005, DM-REQ-006, INV-005 | src/domain/value_objects/core.py, src/domain/value_objects/__init__.py, tests/domain/test_value_objects.py |
| P1-T02 | Implement aggregate roots and entities | 03, 12 | DMI-002, DMI-006, DMI-007, DMI-008, DMI-009, DMI-010, DMI-011 | src/domain/entities/core.py, src/domain/entities/__init__.py, tests/domain/test_entities.py |
| P1-T03 | Implement domain invariants service | 03, 12 | DMI-001, DMI-002, DMI-003, DMI-004, DMI-005, DMI-006, DMI-007, DMI-008, DMI-009, DMI-010, DMI-011, DMI-012, DMI-013, DMI-014, DMI-015 | src/domain/services/invariants.py, src/domain/services/invariant_errors.py, tests/domain/test_invariants_service.py |
| P1-T04 | Implement Business Fact model | 04, 12 | BF-001, BF-002, BF-003, BF-004, BF-005 | src/business_facts/models/facts.py, src/business_facts/models/__init__.py, tests/business_facts/test_business_fact_model.py |
| P1-T05 | Implement Business Fact validators | 04, 12 | BF-002, BF-003, BF-004, BF-005 | src/business_facts/validators/pipeline.py, src/business_facts/validators/__init__.py, tests/business_facts/test_business_fact_validators.py |

## 5.2 Update Rule

For each completed task:

1. Add one matrix row.
2. Reference at least one rule ID and one source document.
3. Link evidence to concrete files or commands.

---

# 6. Diagrams

No diagram required.

---

# 7. Data Models

Traceability row fields: task_id, title, sources, rule_ids, evidence.

---

# 8. Interfaces

This matrix is consumed by task closure reviews and phase gate checks.

---

# 9. Error Handling

If a task cannot be mapped to rule IDs, it cannot be closed and must be reviewed for scope or documentation gaps.

---

# 10. Future Improvements

- Add requirement-level mapping columns when REQ identifiers are formalized.

---

# 11. Changelog

## 1.0.0

- Created task-to-rule traceability matrix for Phase 0 execution.

## 1.1.0

- Added P0-T06 mapping for sample data policy and data/meetings conventions.

## 1.2.0

- Added P1-T01 mapping for immutable value objects and validation test coverage.

## 1.3.0

- Added P1-T02 mapping for entity identity stability, parent-child constraints and lifecycle validation.

## 1.4.0

- Added P1-T03 mapping for invariant service and explicit typed errors with DMI-001..DMI-015 coverage.

## 1.5.0

- Added P1-T04 mapping for immutable BusinessFact model, typed BF-001..BF-018 catalog, explicit references and append-only log.

## 1.6.0

- Added P1-T05 mapping for fact validation pipeline, immutable-history contradiction detection and traceable validation reasons.
