# 07 - Persistence Model

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Draft

---

## Depends On

- 00-project-design-handbook.md
- 02-domain-ontology.md
- 03-domain-model.md
- 04-business-facts.md
- 05-knowledge-model.md
- 06-processing-pipeline.md

## Followed By

- 08-api-design.md

---

# 1. Purpose

This document defines the conceptual persistence model for the project.

Its purpose is to describe how Business Domain concepts, Business Facts, Knowledge Model outputs and processing artifacts are represented in persistent storage.

Persistence SHALL follow the ontology and domain model.

The ontology and domain model SHALL NOT follow persistence.

---

# 2. Scope

This document covers the persistence design for version 1.

It defines:

- the persistence boundaries between Business Domain, Knowledge Domain and Processing Domain;
- the conceptual storage model for core domain entities;
- the storage approach for Business Facts and knowledge artifacts;
- the required metadata for traceability and restartability;
- the conventions for identifiers, timestamps and soft deletion.

It does not define:

- concrete SQL schema implementation details;
- storage performance tuning;
- UI or API serialization details.

---

# 3. Dependencies

This document depends on the normative sources listed below.

- 00-project-design-handbook.md defines database and storage conventions.
- 02-domain-ontology.md defines the conceptual separation between domains.
- 03-domain-model.md defines the business concepts to persist.
- 04-business-facts.md defines the immutable facts to persist.
- 05-knowledge-model.md defines the derived knowledge structures to persist.
- 06-processing-pipeline.md defines the processing artifacts that require recoverability.

---

# 4. Persistence Principles

## PER-001 — Persistence Follows the Domain

The persistence model SHALL reflect the Business Domain and not redefine it.

## PER-002 — Business Facts Are Authoritative

Business Facts SHALL be stored as immutable records.

## PER-003 — Knowledge Is Derived

Knowledge Model outputs SHALL be stored as derived artifacts linked to supporting facts.

## PER-004 — Processing Artifacts Are Separate

Processing artifacts SHALL be stored separately from Business Domain entities.

## PER-005 — Soft Deletion

Business data SHALL NOT be physically deleted.

Deleted records SHALL be marked with a deletion timestamp.

---

# 5. Persistence Boundaries

## 5.1 Business Domain Storage

The following concepts are stored as Business Domain records:

- Organization
- Meeting
- Person
- Participant
- Agenda
- Agenda Item
- Discussion
- Intervention
- Motion
- Vote
- Resolution
- Action
- Attachment

## 5.2 Business Fact Storage

Business Facts SHALL be stored as immutable records referencing one or more business concepts.

## 5.3 Knowledge Domain Storage

Knowledge artifacts SHALL be stored as derived records linked to Business Facts.

Examples:

- Summary
- Detected Topic
- Detected Decision
- Detected Deadline
- Detected Reference
- Evidence
- Confidence Score
- Semantic Relationship

## 5.4 Processing Domain Storage

Processing artifacts SHALL be stored separately from the Business Domain and include:

- audio artifacts;
- transcript segments;
- diarization outputs;
- checkpoints;
- logs;
- processing status.

---

# 6. Storage Conventions

## 6.1 Database Engine

PostgreSQL is the normative database engine for the project.

## 6.2 Identifiers

Primary keys SHALL use UUIDv7.

## 6.3 Timestamps

All timestamps SHALL be stored in UTC.

## 6.4 Soft Delete

Every business record SHALL include a deletion timestamp field named deleted_at.

## 6.5 Naming Conventions

Table and column names SHALL use snake_case.

---

# 7. Conceptual Data Model

This section defines the persistence structure conceptually.

## 7.1 Organization

Conceptual fields:

- id
- name
- created_at
- updated_at
- deleted_at

## 7.2 Meeting

Conceptual fields:

- id
- organization_id
- title
- started_at
- closed_at
- status
- created_at
- updated_at
- deleted_at

## 7.3 Person

Conceptual fields:

- id
- organization_id
- full_name
- email_address
- created_at
- updated_at
- deleted_at

## 7.4 Participant

Conceptual fields:

- id
- meeting_id
- person_id
- role
- joined_at
- left_at
- created_at
- updated_at
- deleted_at

## 7.5 Agenda

Conceptual fields:

- id
- meeting_id
- title
- created_at
- updated_at
- deleted_at

## 7.6 Agenda Item

Conceptual fields:

- id
- agenda_id
- title
- position
- created_at
- updated_at
- deleted_at

## 7.7 Discussion

Conceptual fields:

- id
- meeting_id
- agenda_item_id
- title
- started_at
- closed_at
- created_at
- updated_at
- deleted_at

## 7.8 Intervention

Conceptual fields:

- id
- discussion_id
- participant_id
- text_reference
- started_at
- ended_at
- created_at
- updated_at
- deleted_at

## 7.9 Motion

Conceptual fields:

- id
- discussion_id
- text
- status
- created_at
- updated_at
- deleted_at

## 7.10 Vote

Conceptual fields:

- id
- motion_id
- status
- vote_count
- created_at
- updated_at
- deleted_at

## 7.11 Resolution

Conceptual fields:

- id
- meeting_id
- motion_id
- outcome
- created_at
- updated_at
- deleted_at

## 7.12 Action

Conceptual fields:

- id
- meeting_id
- resolution_id
- description
- status
- created_at
- updated_at
- deleted_at

## 7.13 Attachment

Conceptual fields:

- id
- meeting_id
- file_name
- file_uri
- created_at
- updated_at
- deleted_at

---

# 8. Business Facts Storage

Business Facts SHALL be persisted as immutable records.

## 8.1 Business Fact Record

Conceptual fields:

- id
- meeting_id
- fact_type
- occurred_at
- payload
- created_at
- deleted_at

## 8.2 Fact Relationships

A Business Fact SHALL be able to reference:

- one or more entities;
- one or more value objects where relevant;
- one or more supporting evidence references.

## 8.3 Immutability Rule

A Business Fact SHALL NOT be updated in place.

If a correction is needed, a new fact SHALL be created.

---

# 9. Knowledge Storage

Knowledge artifacts SHALL be stored as derived records linked to supporting facts.

## 9.1 Summary

Conceptual fields:

- id
- meeting_id
- text
- created_at
- updated_at
- deleted_at

## 9.2 Detected Topic

Conceptual fields:

- id
- meeting_id
- label
- confidence
- created_at
- updated_at
- deleted_at

## 9.3 Detected Decision

Conceptual fields:

- id
- meeting_id
- decision_type
- confidence
- created_at
- updated_at
- deleted_at

## 9.4 Detected Deadline

Conceptual fields:

- id
- meeting_id
- due_at
- confidence
- created_at
- updated_at
- deleted_at

## 9.5 Detected Reference

Conceptual fields:

- id
- meeting_id
- reference_type
- reference_value
- created_at
- updated_at
- deleted_at

## 9.6 Evidence

Conceptual fields:

- id
- knowledge_element_id
- fact_id
- evidence_text
- created_at
- updated_at
- deleted_at

## 9.7 Semantic Relationship

Conceptual fields:

- id
- meeting_id
- source_element_id
- target_element_id
- relationship_type
- created_at
- updated_at
- deleted_at

---

# 10. Processing Artifact Storage

Processing artifacts SHALL be stored in a separate logical area.

## 10.1 Processing Record

Conceptual fields:

- id
- meeting_id
- stage_name
- status
- started_at
- finished_at
- correlation_id
- created_at
- updated_at
- deleted_at

## 10.2 Checkpoint Record

Conceptual fields:

- id
- meeting_id
- stage_name
- checkpoint_data
- created_at
- updated_at
- deleted_at

## 10.3 Log Record

Conceptual fields:

- id
- meeting_id
- worker_id
- correlation_id
- level
- message
- created_at
- updated_at
- deleted_at

---

# 11. Relationship Model

The storage model SHALL preserve the following logical relationships.

- Organization contains Meetings.
- Meeting contains Participants, Discussions, Agenda, Attachments and Business Facts.
- Agenda contains Agenda Items.
- Discussion contains Interventions and Motions.
- Motion may generate Vote and Resolution.
- Resolution may create Action.
- Business Facts reference Business Concepts.
- Knowledge elements reference Business Facts and business concepts.

---

# 12. Traceability Requirements

Every persisted record SHALL support traceability.

Minimum requirements:

- record id;
- meeting id;
- timestamp;
- provenance reference;
- supporting evidence reference where applicable.

---

# 13. Error Handling

## 13.1 Recoverable Errors

- transient processing failure;
- incomplete evidence;
- delayed enrichment of derived facts.

Action: store the partial state and continue or retry safely.

## 13.2 Fatal Errors

- invalid meeting context;
- invalid relationship to a parent entity;
- attempt to overwrite an immutable Business Fact.

Action: stop the affected persistence operation and preserve the evidence for review.

---

# 14. Open Questions

The following questions remain open for future refinement.

- Should the knowledge layer be stored in one table per concept or in a common knowledge table?
- Should evidence be stored inline or as separate normalized records?
- Should processing artifacts be separated physically or only logically?

---

# 15. Future Improvements

- Add explicit schema examples for PostgreSQL tables.
- Define indexes and partitioning strategy for large meeting histories.
- Add a formal persistence conformance checklist.

---

# 16. Changelog

## 1.0.0

- Created the initial conceptual persistence model.
- Aligned persistence boundaries with the Business Domain, Knowledge Domain and Processing Domain.
- Defined the main conceptual records for domain entities, Business Facts and knowledge artifacts.
