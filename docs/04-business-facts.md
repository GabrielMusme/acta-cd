# 04 - Business Facts

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Draft

---

## Depends On

- 00-project-design-handbook.md
- 01-domain-discovery.md
- 02-domain-ontology.md
- 03-domain-model.md

## Followed By

- 05-knowledge-model.md
- 06-processing-pipeline.md
- 07-persistence-model.md

---

# 1. Purpose

This document defines the catalog of Business Facts recognized by the Business Domain.

Its purpose is to make explicit the immutable, objective occurrences that constitute the historical record of a meeting.

Business Facts are the authoritative source of truth for objective reality.

They are not interpretations and they are not generated documents.

---

# 2. Scope

This document covers the business facts required for version 1 of the system.

It defines:

- business fact identifiers;
- semantic meaning;
- triggering business context;
- participating concepts;
- preconditions;
- consequences;
- traceability to the Domain Model.

It does not define:

- AI prompts;
- processing workers;
- persistence schema;
- document formatting.

---

# 3. Dependencies

This document depends on the normative sources listed below.

- 00-project-design-handbook.md defines governance and architecture constraints.
- 02-domain-ontology.md defines the ontological category and invariants for Business Facts.
- 03-domain-model.md defines the business concepts and the catalog of facts used here.

---

# 4. Business Fact Principles

## BF-001

Every Business Fact SHALL describe an objective occurrence.

## BF-002

Every Business Fact SHALL be immutable.

## BF-003

Every Business Fact SHALL belong to exactly one Meeting.

## BF-004

Every Business Fact SHALL reference one or more business concepts from the Domain Model.

## BF-005

Business Facts SHALL NOT redefine business concepts; they only record occurrences.

---

# 5. Business Fact Catalog

## 5.1 Meeting Lifecycle Facts

### BF-001 — Meeting Created

Purpose: records the existence of a new meeting in the business domain.

Participants: Organization, Meeting.

Preconditions: an Organization exists and a Meeting is formally initiated.

Consequences: the Meeting becomes part of the historical record.

Traceability: Domain Model section 8.2.

### BF-002 — Meeting Started

Purpose: records the effective beginning of the meeting.

Participants: Meeting.

Preconditions: the Meeting exists.

Consequences: subsequent participation and discussion facts become attributable to the meeting.

Traceability: Domain Model section 8.2.

### BF-003 — Meeting Closed

Purpose: records the formal closure of the meeting.

Participants: Meeting.

Preconditions: the Meeting is active.

Consequences: the meeting enters historical closure state without losing identity.

Traceability: Domain Model section 8.2.

## 5.2 Participation Facts

### BF-004 — Participant Joined

Purpose: records that a Participant became part of the meeting.

Participants: Participant, Meeting, Person.

Preconditions: the Person exists and the Participant is created for the Meeting.

Consequences: the participation becomes part of the historical record.

Traceability: Domain Model section 9.2.

### BF-005 — Participant Left

Purpose: records that a Participant ceased participating in the meeting.

Participants: Participant, Meeting.

Preconditions: the Participant was previously joined.

Consequences: the participation history remains intact and the exit becomes part of the historical record.

Traceability: Domain Model section 9.2.

## 5.3 Agenda and Discussion Facts

### BF-006 — Agenda Loaded

Purpose: records that an Agenda was associated with the Meeting.

Participants: Meeting, Agenda.

Preconditions: the Agenda exists and belongs to the Meeting.

Consequences: agenda-based discussion structure becomes available.

Traceability: Domain Model section 9.3.

### BF-007 — Discussion Started

Purpose: records that a Discussion began.

Participants: Discussion, Meeting, Agenda Item.

Preconditions: the Discussion exists and belongs to the Meeting.

Consequences: interventions and motions may be associated with the Discussion.

Traceability: Domain Model section 9.5.

### BF-008 — Discussion Closed

Purpose: records that a Discussion ended.

Participants: Discussion, Meeting.

Preconditions: the Discussion was previously started.

Consequences: the discussion state becomes historical and no longer active.

Traceability: Domain Model section 9.5.

## 5.4 Motion and Vote Facts

### BF-009 — Motion Proposed

Purpose: records that a Motion was proposed within a Discussion.

Participants: Motion, Discussion.

Preconditions: the Discussion exists.

Consequences: the Motion becomes available for subsequent deliberation and vote.

Traceability: Domain Model section 9.7.

### BF-010 — Motion Amended

Purpose: records a change to the content or scope of an existing Motion.

Participants: Motion, Discussion.

Preconditions: the Motion exists.

Consequences: the Motion history preserves the amendment as a new fact.

Traceability: Domain Model section 9.7.

### BF-011 — Motion Withdrawn

Purpose: records that a Motion was withdrawn.

Participants: Motion, Discussion.

Preconditions: the Motion exists.

Consequences: the Motion becomes inactive without destroying its historical identity.

Traceability: Domain Model section 9.7.

### BF-012 — Vote Started

Purpose: records that a Vote process began for a Motion.

Participants: Vote, Motion.

Preconditions: the Motion exists.

Consequences: a Vote entity becomes active.

Traceability: Domain Model section 9.8.

### BF-013 — Vote Closed

Purpose: records that a Vote process ended.

Participants: Vote, Motion.

Preconditions: the Vote started.

Consequences: the outcome becomes part of the historical record.

Traceability: Domain Model section 9.8.

## 5.5 Resolution and Action Facts

### BF-014 — Resolution Approved

Purpose: records that a Resolution was approved.

Participants: Resolution, Motion.

Preconditions: the Resolution exists and addresses a Motion.

Consequences: the meeting outcome becomes explicit.

Traceability: Domain Model section 9.9.

### BF-015 — Resolution Rejected

Purpose: records that a Resolution was rejected.

Participants: Resolution, Motion.

Preconditions: the Resolution exists and addresses a Motion.

Consequences: the outcome becomes explicit.

Traceability: Domain Model section 9.9.

### BF-016 — Action Assigned

Purpose: records that an Action was created from a Resolution.

Participants: Action, Resolution.

Preconditions: the Resolution exists.

Consequences: assignment responsibility becomes part of the business record.

Traceability: Domain Model section 9.10.

### BF-017 — Action Completed

Purpose: records that an Action reached completion.

Participants: Action, Resolution.

Preconditions: the Action exists.

Consequences: completion status becomes part of the historical business record.

Traceability: Domain Model section 9.10.

## 5.6 Reference Facts

### BF-018 — Document Referenced

Purpose: records that a document or attachment became part of an explicit business reference.

Participants: Attachment, Meeting, Document reference context.

Preconditions: the attachment or document exists in the meeting context.

Consequences: the reference becomes part of the evidentiary record.

Traceability: Domain Model section 9.11.

---

# 6. Relationships Between Facts and Concepts

Business Facts are the bridge between the Business Domain and the Knowledge Domain.

Each fact references a set of base concepts from the Domain Model.

The relation is one-way:

Business Domain -> Knowledge Domain.

The Knowledge Domain may interpret facts, but it shall not redefine them.

---

# 7. Error Handling

## 7.1 Recoverable Errors

- A fact is missing but the related concept already exists.
- An optional supporting reference arrives late.

Action: preserve the existing facts and record a corrective or supplementary fact if required.

## 7.2 Fatal Errors

- A fact lacks a Meeting reference.
- A fact references a non-existent business concept.
- A fact contradicts an immutable prior fact without a new corrective fact.

Action: stop propagation of the invalid state and require correction.

---

# 8. Open Questions

The current catalog remains intentionally minimal for version 1.

Open questions may require future fact refinement:

- Should a fact distinguish between formal agenda item postponement and cancellation?
- Should resolution outcomes require more than approved/rejected?
- Should attachments require a specialized fact taxonomy?

---

# 9. Changelog

## 1.0.0

- Created initial Business Facts document for version 1.
- Aligned fact catalog with Domain Model concepts and ontology invariants.
- Added principles, semantics, and error handling.
