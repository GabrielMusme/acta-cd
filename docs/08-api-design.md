# 08 - API Design

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
- 07-persistence-model.md

---

# 1. Purpose

This document defines the conceptual external interface of the system.

Its purpose is to describe the API surface exposed to clients without redefining the Business Domain.

The API SHALL expose capabilities such as meeting intake, retrieval of business concepts, knowledge review and export-oriented operations.

---

# 2. Scope

This document covers the API design for version 1.

It defines:

- the main resources exposed by the system;
- the operations available for each resource;
- the request and response model shape;
- the rules for status codes, error handling and authentication concepts;
- the relationship between API contracts and the Domain Model.

It does not define:

- implementation code;
- frontend UI details;
- storage schema;
- prompt engineering.

---

# 3. Dependencies

This document depends on the normative sources listed below.

- 00-project-design-handbook.md defines API conventions and governance.
- 02-domain-ontology.md defines the conceptual separation between business reality and interface concerns.
- 03-domain-model.md defines the business concepts that APIs expose.
- 04-business-facts.md defines the immutable facts that may be queried or represented.
- 05-knowledge-model.md defines derived knowledge outputs that can be exposed.
- 06-processing-pipeline.md defines the processing stages that may be started or monitored.
- 07-persistence-model.md defines the persisted entities behind the API.

---

# 4. API Principles

## API-001 — Domain Respect

The API SHALL NOT redefine business concepts.

It SHALL expose them through stable contracts.

## API-002 — JSON and REST

The API SHALL use REST principles and JSON payloads.

## API-003 — UTF-8 and ISO-8601

All payloads SHALL use UTF-8 and ISO-8601 timestamps.

## API-004 — Explicit Errors

Errors SHALL use standard HTTP semantics and include actionable detail.

## API-005 — Traceability

API responses SHALL preserve enough information to trace the resulting state back to the relevant Business Facts and knowledge elements.

---

# 5. API Architecture Overview

The API exposes a small set of coherent resources.

Conceptually:

- Meetings
- Participants
- Discussions
- Motions
- Resolutions
- Actions
- Business Facts
- Knowledge Model outputs
- Processing jobs

These resources are accessed through standard CRUD-like operations and a small set of workflow-oriented operations.

---

# 6. Resource Model

## 6.1 Meeting Resource

Represents a Meeting as defined in the Domain Model.

Operations:

- POST /meetings
- GET /meetings/{meeting_id}
- GET /meetings
- PATCH /meetings/{meeting_id}

Representative response fields:

- id
- organization_id
- title
- status
- started_at
- closed_at
- created_at
- updated_at

## 6.2 Participant Resource

Represents a Participant linked to a Meeting and a Person.

Operations:

- POST /meetings/{meeting_id}/participants
- GET /meetings/{meeting_id}/participants
- GET /meetings/{meeting_id}/participants/{participant_id}

Representative response fields:

- id
- meeting_id
- person_id
- role
- joined_at
- left_at

## 6.3 Discussion Resource

Represents a Discussion belonging to a Meeting.

Operations:

- POST /meetings/{meeting_id}/discussions
- GET /meetings/{meeting_id}/discussions
- GET /meetings/{meeting_id}/discussions/{discussion_id}

Representative response fields:

- id
- meeting_id
- agenda_item_id
- title
- started_at
- closed_at

## 6.4 Motion Resource

Represents a Motion contained in a Discussion.

Operations:

- POST /meetings/{meeting_id}/discussions/{discussion_id}/motions
- GET /meetings/{meeting_id}/discussions/{discussion_id}/motions
- GET /meetings/{meeting_id}/discussions/{discussion_id}/motions/{motion_id}

Representative response fields:

- id
- discussion_id
- text
- status

## 6.5 Resolution Resource

Represents a Resolution addressing a Motion.

Operations:

- POST /meetings/{meeting_id}/resolutions
- GET /meetings/{meeting_id}/resolutions
- GET /meetings/{meeting_id}/resolutions/{resolution_id}

Representative response fields:

- id
- meeting_id
- motion_id
- outcome

## 6.6 Action Resource

Represents an Action originating from a Resolution.

Operations:

- POST /meetings/{meeting_id}/actions
- GET /meetings/{meeting_id}/actions
- GET /meetings/{meeting_id}/actions/{action_id}

Representative response fields:

- id
- meeting_id
- resolution_id
- description
- status

## 6.7 Business Fact Resource

Represents an immutable Business Fact.

Operations:

- GET /meetings/{meeting_id}/business-facts
- GET /meetings/{meeting_id}/business-facts/{fact_id}

Representative response fields:

- id
- meeting_id
- fact_type
- occurred_at
- payload

## 6.8 Knowledge Resource

Represents knowledge derived from Business Facts.

Operations:

- GET /meetings/{meeting_id}/knowledge
- GET /meetings/{meeting_id}/knowledge/summary
- GET /meetings/{meeting_id}/knowledge/decisions
- GET /meetings/{meeting_id}/knowledge/deadlines

Representative response fields:

- meeting_id
- summary
- detected_topics
- detected_decisions
- detected_deadlines
- evidence
- confidence

## 6.9 Processing Job Resource

Represents a processing operation for a Meeting.

Operations:

- POST /meetings/{meeting_id}/jobs
- GET /meetings/{meeting_id}/jobs
- GET /meetings/{meeting_id}/jobs/{job_id}

Representative response fields:

- id
- meeting_id
- status
- created_at
- updated_at

---

# 7. Request and Response Conventions

## 7.1 Request Payloads

Request bodies SHALL be JSON objects.

Required fields SHALL be explicit.

Optional fields SHALL be nullable or omitted.

## 7.2 Response Payloads

Responses SHALL include:

- data
- metadata where relevant
- traceability references where applicable

Example response envelope:

```json
{
  "data": {},
  "meta": {
    "meeting_id": "...",
    "traceability": ["fact:...", "evidence:..."]
  }
}
```

## 7.3 Pagination

List endpoints SHALL support pagination where the result set may grow.

Recommended fields:

- limit
- offset
- total

---

# 8. Status Codes

The API SHALL use standard HTTP status codes.

## 8.1 Success Codes

- 200 OK
- 201 Created
- 202 Accepted

## 8.2 Client Error Codes

- 400 Bad Request
- 404 Not Found
- 409 Conflict

## 8.3 Server Error Codes

- 500 Internal Server Error
- 503 Service Unavailable

---

# 9. Error Handling

Errors SHALL be returned as structured JSON payloads.

Example:

```json
{
  "error": {
    "code": "meeting_not_found",
    "message": "The requested meeting does not exist.",
    "details": []
  }
}
```

## 9.1 Recoverable Errors

- transient processing failure
- temporary resource unavailability

Action: return 503 or 202 where appropriate.

## 9.2 Fatal Errors

- invalid domain state
- business rule violation
- attempt to overwrite immutable facts

Action: return 400 or 409 with explicit explanation.

---

# 10. Authentication and Authorization Concepts

This document defines conceptual requirements only.

The system SHALL support authenticated access for administrative or review use cases.

At minimum:

- authentication mechanism to be defined later;
- authorization rules per resource type;
- auditability of operator actions.

---

# 11. API and Domain Model Relationship

The API SHALL expose the Domain Model through interface contracts.

It SHALL NOT create new concepts or redefine the meaning of existing ones.

The following rule is normative:

API contracts SHALL remain aligned with the Business Domain and the Knowledge Model.

---

# 12. Open Questions

The following questions remain open for future refinement.

- Should the API expose raw processing artifacts to operators only?
- Should knowledge outputs be read-only or editable through the API?
- Should export operations be part of the API or handled as background jobs?

---

# 13. Future Improvements

- Add authentication and authorization design.
- Define OpenAPI schemas for each resource.
- Add example request and response payloads per endpoint.
- Add rate limiting and observability requirements.

---

# 14. Changelog

## 1.0.0

- Created the initial conceptual API design document.
- Aligned API resources with the Domain Model, Business Facts and Knowledge Model.
- Defined resource structure, status codes and error handling conventions.
