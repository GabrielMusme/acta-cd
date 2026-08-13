# 00 - Project Design Handbook

**Project:**

**Version:** 1.0

**Status:** Approved

**Last Update:** 2026-07-22

---

# Table of Contents

1. Purpose
2. Project Objectives
3. Scope
4. Architecture Principles
5. Development Principles
6. Documentation Standards
7. Naming Conventions
8. Source Code Conventions
9. Database Conventions
10. Storage Conventions
11. AI/LLM Conventions
12. API Conventions
13. Logging Standards
14. Error Handling
15. Versioning
16. Decision Records
17. Traceability
18. Document Template
19. Worker Template
20. Prompt Template
21. Future Changes

---

# 1. Purpose

This document defines the mandatory design rules that govern the entire project.

Every document in the `docs` folder must comply with this handbook.

If any document contradicts this handbook, this handbook prevails.

---

# 2. Project Objectives

The system shall:

- Generate meeting minutes from audio recordings.
- Execute completely on local infrastructure.
- Use only Free/Open Source technologies.
- Be fully reproducible.
- Be restartable after failures.
- Produce traceable results.

---

# 3. Scope

Version 1 includes:

- Audio upload
- Audio preprocessing
- Speech transcription
- Speaker diarization
- Knowledge extraction
- Minutes generation
- Human review
- DOCX export
- PDF export
- Markdown export

Out of scope:

- Live transcription
- Real-time captioning
- Cloud execution
- Commercial APIs

---

# 4. Architecture Principles

## ARCH-001

The system SHALL operate completely offline.

---

## ARCH-002

The original audio SHALL NEVER be modified.

---

## ARCH-003

Every processing stage SHALL be restartable.

---

## ARCH-004

The database SHALL be the single source of truth.

---

## ARCH-005

Knowledge extraction SHALL be independent from document generation.

---

## ARCH-006

Generated documents SHALL NEVER be used as input for future processing.

Only structured data may be reused.

---

## ARCH-007

The canonical representation of a meeting SHALL be the Knowledge Model.

---

## ARCH-008

The Processing Model SHALL remain independent from the Domain Model.

The Processing Model represents how the system operates.

The Domain Model represents the business concepts extracted from the meeting.

No processing entity shall leak into the business domain.

---

## ARCH-009

The Domain Model SHALL represent the objective facts of the meeting.

It SHALL NOT model the personal workflow of the meeting secretary.

Meeting minutes are a representation of the Domain Model, not the Domain Model itself.

---

# 5. Development Principles

- Keep components loosely coupled.
- Prefer composition over inheritance.
- Prefer explicit code over magic.
- Avoid premature optimization.
- Every module shall have a single responsibility.

---

# 6. Documentation Standards

## Standard Structure

Every document shall contain:

- Purpose
- Scope
- Dependencies
- Design
- Diagrams
- Data Models
- Interfaces
- Error Handling
- Future Improvements
- Changelog

---

## Documentation Governance

### DOC-001

Project documentation constitutes the authoritative source of architectural knowledge.

---

### DOC-002

No architectural decision SHALL exist exclusively within conversations, emails or meeting notes.

Every accepted architectural decision SHALL be incorporated into the appropriate project document before implementation continues.

---

### DOC-003

Conversations are considered design workspaces.

Project documents are considered normative specifications.

---

### DOC-004

If a discrepancy exists between a conversation and the documentation, the documentation prevails until formally revised.

---

### DOC-005

No implementation SHALL depend upon undocumented architectural decisions.

---

## Concept Ownership

### DOC-006

Every business concept SHALL be defined exactly once within the project documentation.

---

### DOC-007

Subsequent documents MAY reference a concept.

They SHALL NOT redefine it.

---

### DOC-008

The document that defines a concept becomes its authoritative source.

---

## Document Dependencies

### DOC-009

Every document SHALL explicitly declare its dependencies.

---

### DOC-010

A document MAY depend only upon documents with a lower sequence number.

---

### DOC-011

Circular dependencies between project documents are prohibited.

---

### DOC-012

Whenever a document introduces a new business concept, the author SHALL verify that the concept has not already been defined elsewhere.

If the concept already exists, it shall be referenced rather than redefined.

---

# 7. Naming Conventions

## Database

snake_case

Example

meeting_segments

---

## Source Code

camelCase

Example

meetingRepository

---

## Classes

PascalCase

MeetingRepository

---

## Constants

UPPER_CASE

MAX_SEGMENT_DURATION

---

## Files

kebab-case

meeting-service.ts

---

# 8. Source Code Conventions

Programming language naming:

Python

PEP8

TypeScript

ESLint + Prettier

Every public function must include documentation.

Every module shall have unit tests.

---

# 9. Database Conventions

Database:

PostgreSQL

Primary Keys:

UUIDv7

Timestamps:

UTC

Soft Delete:

deleted_at

Never delete business data physically.

---

# 10. Storage Conventions

Each meeting shall have its own workspace.

Example

/data/

meeting_000001/

original/

audio/

segments/

knowledge/

output/

logs/

---

# 11. AI Conventions

LLMs SHALL NEVER return free text when structured information is expected.

Every extraction prompt shall return JSON.

Every JSON shall be validated using Pydantic.

Hallucinated fields SHALL be rejected.

Every prompt shall have a version number.

---

# 12. API Conventions

REST

JSON

UTF-8

ISO-8601 dates

HTTP status codes shall follow RFC specifications.

---

# 13. Logging

Every worker shall generate:

- processing time
- errors
- retries
- memory usage
- CPU usage

Every log entry shall contain:

- timestamp
- meeting_id
- worker_id
- correlation_id

---

# 14. Error Handling

Recoverable errors:

Retry.

Fatal errors:

Stop processing.

Unexpected errors:

Log + Notify.

---

# 15. Versioning

Documentation:

Semantic Versioning

Example

1.2.0

Prompt versions are independent.

---

# 16. Decision Records

Every architectural decision shall receive an identifier.

Example

DEC-001

DEC-002

DEC-003

Decisions are immutable.

If modified:

Create a new decision.

---

# 17. Traceability

Every important implementation shall reference:

Requirement

Architecture Principle

Decision

Example

Implements:

ARCH-003

DEC-014

REQ-022

---

# 18. Standard Document Template

Every document shall follow:

Purpose

Scope

Definitions

Requirements

Design

Implementation

Open Questions

Future Improvements

Changelog

---

# 19. Worker Template

Purpose

Inputs

Outputs

Dependencies

Processing

Retries

Logging

Metrics

Errors

---

# 20. Prompt Template

Identifier

Version

Purpose

Model

Temperature

Input Schema

Output Schema

Examples

Validation Rules

Failure Conditions

---

# 21. Future Changes

Every modification to this handbook requires:

- version increment
- changelog update
- impact analysis
- review of affected documents

---
