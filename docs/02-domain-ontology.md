# 02 - Domain Ontology

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.1

**Status:** Stable

---

## Depends On

- 00-project-design-handbook.md
- 01-domain-discovery.md

## Followed By

- 03-domain-model.md
- 04-business-facts.md
- 05-knowledge-model.md

---

# 1. Purpose

This document defines the Business Ontology of the Intelligent Meeting Minutes Engine.

Its purpose is to establish the fundamental concepts that exist within the business domain independently of any software implementation.

The ontology answers questions such as:

- What exists?
- What objectively occurs?
- Which concepts possess identity?
- Which concepts evolve over time?
- Which concepts are immutable?
- How are business concepts related?

This document intentionally excludes implementation details such as databases, APIs, programming languages, user interfaces and Artificial Intelligence models.

Its purpose is not to describe software.

Its purpose is to describe business reality.

Every subsequent design document shall conform to the concepts defined herein.

---

# 2. Scope

This ontology defines the conceptual structure of the Business Domain.

It specifies:

- business concepts;
- conceptual categories;
- identity semantics;
- temporal semantics;
- structural relationships;
- business invariants.

This ontology does **not** define:

- software architecture;
- persistence mechanisms;
- processing pipelines;
- Artificial Intelligence;
- prompt engineering;
- APIs;
- communication protocols.

Those concerns are addressed by subsequent project documents.

---

# 3. Design Goals

The ontology has been designed according to the following objectives.

---

## GOAL-001

Represent business reality independently of any implementation technology.

---

## GOAL-002

Provide a common conceptual vocabulary shared by every component of the project.

---

## GOAL-003

Separate objective business reality from its computational interpretation.

---

## GOAL-004

Support multiple organizations and meeting types without requiring structural changes.

---

## GOAL-005

Remain stable even if implementation technologies evolve.

---

# 4. Business Reality

Meetings exist independently of software.

A meeting may occur without:

- audio recording;
- transcription;
- minutes;
- Artificial Intelligence.

The software neither creates nor modifies business reality.

Its sole responsibility is to observe, represent and organize that reality.

The ontology therefore models the meeting itself rather than the software that processes it.

---

# 5. Fundamental Principles

The following principles govern every concept defined by this ontology.

---

## ONT-001 — Reality First

Business reality always precedes software.

Software is only a representation of business reality.

Whenever a discrepancy exists between software and reality, reality prevails.

---

## ONT-002 — Objective Business Reality

The Business Domain consists of:

- persistent business concepts;
- objective business facts.

Persistent concepts describe what exists.

Business Facts describe what objectively occurred.

Interpretations are not part of the Business Domain.

---

## ONT-003 — Identity Before Attributes

Business concepts are primarily defined by their identity.

Attributes may change during the lifetime of a concept.

Identity shall remain stable.

---

## ONT-004 — Immutability of Business Facts

Business Facts are immutable.

If business reality changes, new Business Facts shall be created.

Historical information shall never be rewritten.

---

## ONT-005 — Explicit Relationships

Relationships between business concepts are themselves part of the ontology.

They are not implementation details.

Every relationship shall represent a real dependency that exists in the business domain.

---

## ONT-006 — Technology Independence

No ontological concept shall depend upon:

- programming language;
- database technology;
- framework;
- communication protocol;
- Artificial Intelligence implementation.

---

## ONT-007 — Single Meaning

Each ontological concept shall possess one and only one business meaning.

Different concepts shall never share the same definition.

Likewise, one concept shall never possess multiple business meanings.

---

## ONT-008 — Extensibility

The ontology shall support future organizational structures without requiring conceptual redesign.

Institution-specific behavior shall be introduced through specialization rather than modification.

---

# 6. Ontological Categories

Every business concept belongs to exactly one ontological category.

The Business Domain recognizes the following categories.

- Aggregate Root
- Entity
- Value Object
- Business Fact
- Relationship

These categories are exhaustive for the current scope of the Business Domain.

No additional categories shall be introduced unless a genuine conceptual distinction cannot be represented by one of the existing categories.

---

# 7. Business Domain and Knowledge Domain

One of the fundamental architectural decisions of this project is the explicit separation between business reality and business interpretation.

The project is divided into two conceptual domains.

---

## 7.1 Business Domain

The Business Domain represents objective business reality.

It contains:

- Organizations;
- Meetings;
- Persons;
- Participants;
- Discussions;
- Motions;
- Resolutions;
- Actions;
- Business Facts.

Everything contained within the Business Domain represents objective concepts that exist independently of software.

---

## 7.2 Knowledge Domain

The Knowledge Domain represents the interpretation of business reality.

It contains semantic structures derived from Business Facts, including:

- summaries;
- inferred topics;
- semantic relationships;
- evidence chains;
- confidence assessments.

The Knowledge Domain SHALL NOT redefine business concepts.

Its responsibility is limited to interpreting them.

The Knowledge Domain is defined by the document:

> **05-knowledge-model.md**

---

## 7.3 Dependency Rule

The relationship between both domains is strictly unidirectional.

```
Business Domain
        │
        ▼
Knowledge Domain
```

The Business Domain does not depend upon the Knowledge Domain.

The Knowledge Domain depends exclusively upon the Business Domain.

No interpretation may modify business reality.

Business Facts remain the authoritative source of truth for objective business reality.

The Knowledge Model is the canonical derived representation used to generate human-readable artifacts.

---

# 8. Conceptual View

```
                    Business Reality
                            │
                            ▼
                   Business Domain
                            │
                 Business Facts
                            │
                            ▼
                  Knowledge Domain
                            │
                            ▼
                Human-readable Artifacts
```

Business Facts constitute the observable evidence of business reality.

The Knowledge Domain derives interpretations from those facts.

Human-readable artifacts (minutes, summaries, reports and similar documents) are generated from the Knowledge Domain.

Information flows exclusively downward.

Reverse dependencies are not permitted.

---

# 9. Normative Language

The keywords SHALL, SHALL NOT, SHOULD, SHOULD NOT and MAY are interpreted according to RFC 2119.

Normative statements contained in this ontology take precedence over every subsequent design document.

If a later document contradicts this ontology, the ontology shall prevail until formally revised.

---

# End of Part 1

# 10. Ontological Categories

Every concept belonging to the Business Domain shall belong to exactly one ontological category.

The ontology defines five categories.

1. Aggregate Root
2. Entity
3. Value Object
4. Business Fact
5. Relationship

These categories describe the nature of business concepts.

They do not prescribe software implementation.

---

# 11. Aggregate Root

## Definition

An Aggregate Root represents an autonomous business concept that establishes the primary boundary of a coherent portion of business reality.

It possesses an independent identity.

Its existence does not depend upon any other business concept.

---

## Characteristics

Every Aggregate Root:

- possesses persistent identity;
- exists independently;
- may contain other business concepts;
- defines a coherent business context;
- may exist throughout an extended period of time.

---

## Current Aggregate Roots

Within the current Business Domain the following Aggregate Roots exist.

### Organization

Represents an institution capable of conducting meetings.

Examples include:

- university;
- research institute;
- scientific committee;
- government agency;
- board of directors.

---

### Meeting

Represents one complete meeting held by an Organization.

Every business event described by this ontology occurs within the context of exactly one Meeting.

---

## Non-examples

The following concepts are not Aggregate Roots.

- Discussion
- Motion
- Resolution
- Participant
- Business Fact

Their existence depends upon another business concept.

---

# 12. Entity

## Definition

An Entity represents a distinguishable business concept that possesses its own identity throughout its lifetime.

Two Entities may share identical attributes while representing different real-world concepts.

Identity therefore defines the Entity.

---

## Characteristics

Every Entity:

- possesses identity;
- exists within the context of one Aggregate Root;
- may evolve over time;
- may participate in Business Facts;
- may be described by Value Objects.

---

## Typical Entities

Examples include:

- Person
- Participant
- Discussion
- Agenda
- Agenda Item
- Motion
- Resolution
- Action

The complete list of Entities is defined by the Domain Model.

---

## Lifetime

An Entity continues to exist as long as its corresponding business concept remains part of business reality.

When an Entity completes its business lifecycle it becomes part of the historical record.

Historical Entities shall never lose their identity.

---

## Non-examples

The following concepts are not Entities.

- person's name;
- timestamp;
- confidence score;
- meeting duration;
- vote count.

These concepts describe business concepts rather than possessing their own identity.

---

# 13. Value Object

## Definition

A Value Object represents descriptive information without independent identity.

Its meaning derives entirely from the concept it describes.

Two Value Objects containing equivalent values are considered semantically equivalent.

---

## Characteristics

Every Value Object:

- possesses no identity;
- is immutable;
- is compared by value;
- exists only as part of another business concept.

---

## Examples

Examples include:

- Person Name
- Email Address
- Postal Address
- Time Interval
- Duration
- Date Range
- Vote Count

---

## Non-examples

The following concepts are not Value Objects.

- Meeting
- Discussion
- Motion
- Resolution
- Action

These concepts possess independent identity.

---

# 14. Business Fact

## Definition

A Business Fact represents an objective occurrence observed within business reality.

Business Facts describe events.

They do not describe persistent concepts.

---

## Purpose

Business Facts preserve the objective history of business reality.

They answer one question only.

> What objectively happened?

---

## Characteristics

Every Business Fact:

- occurred once;
- possesses chronological order;
- is immutable;
- belongs to exactly one Meeting;
- references one or more business concepts.

Business Facts never evolve.

Business Facts are never revised.

If reality changes, new Business Facts shall be created.

---

## Typical Business Facts

Examples include:

- Meeting Started
- Meeting Closed
- Discussion Started
- Discussion Closed
- Participant Joined
- Participant Left
- Motion Proposed
- Motion Amended
- Motion Withdrawn
- Vote Started
- Vote Closed
- Resolution Approved
- Resolution Rejected
- Action Assigned
- Action Completed
- Document Referenced

---

## Historical Nature

Business Facts constitute the permanent historical record of business reality.

Business Facts remain valid regardless of future interpretations.

---

# 15. Relationship

## Definition

A Relationship represents a meaningful association between two or more business concepts.

Relationships are themselves part of the ontology.

They are not implementation artifacts.

---

## Characteristics

Every Relationship:

- connects business concepts;
- possesses business meaning;
- defines semantic dependency;
- may define multiplicity;
- may define direction.

Relationships never exist independently.

They exist only by relating business concepts.

---

## Relationship Types

The ontology recognizes three fundamental relationship types.

### Containment

One concept conceptually contains another.

Examples:

- Organization contains Meetings.
- Meeting contains Discussions.
- Meeting contains Participants.

---

### Reference

One concept identifies or refers to another without containing it.

Examples:

- Participant references Person.
- Resolution references Motion.
- Action references Resolution.

---

### Association

Two concepts are semantically related without containment.

Examples:

- Discussion concerns an Agenda Item.
- Motion is discussed during a Discussion.
- Participant contributes to a Discussion.

---

# 16. Category Comparison

The following table summarizes the ontological characteristics of each category.

| Category       | Identity | Mutable | Historical | Represents                   |
| -------------- | -------- | ------- | ---------- | ---------------------------- |
| Aggregate Root | Yes      | Yes     | Yes        | Independent business context |
| Entity         | Yes      | Yes     | Yes        | Persistent business concept  |
| Value Object   | No       | No      | Yes\*      | Descriptive information      |
| Business Fact  | No       | No      | Yes        | Objective occurrence         |
| Relationship   | No       | No      | Yes        | Semantic association         |

\* A Value Object is immutable. Historical persistence depends upon the concept that owns it.

---

# 17. Category Integrity Rules

The following rules apply to every ontological category.

---

### CAT-001

Every business concept SHALL belong to exactly one ontological category.

---

### CAT-002

A concept SHALL NOT migrate from one category to another during its lifecycle.

---

### CAT-003

Identity SHALL exist only for Aggregate Roots and Entities.

---

### CAT-004

Business Facts SHALL reference business concepts but SHALL NOT redefine them.

---

### CAT-005

Relationships SHALL describe semantic dependencies rather than implementation dependencies.

---

### CAT-006

Value Objects SHALL never exist independently of another business concept.

---

# End of Part 2

# 18. Identity

Identity distinguishes one business concept from another.

Identity exists independently of software implementation.

The ontology defines identity as a conceptual property rather than as a technical identifier.

Two business concepts may possess identical descriptive attributes while representing different real-world concepts.

Conversely, a business concept may evolve throughout its lifetime without losing its identity.

Identity therefore remains stable while descriptive information may change.

---

## 18.1 Concepts with Identity

Within the Business Domain, identity exists only for:

- Aggregate Roots;
- Entities.

Identity never belongs to:

- Value Objects;
- Business Facts;
- Relationships.

---

## 18.2 Identity Principles

### ID-001

Identity is intrinsic to the business concept.

It is not created by software.

---

### ID-002

Identity remains stable throughout the entire lifetime of the business concept.

---

### ID-003

Changing descriptive attributes does not change identity.

---

### ID-004

Two different concepts shall never share the same identity.

---

### ID-005

Historical records preserve identity permanently.

Identity is never reassigned.

---

# 19. Participation

Participation represents the involvement of a Person in a specific Meeting.

Participation is represented by the Entity:

Participant

A Participant is not a Person.

Likewise, a Person is not a Participant.

These concepts belong to different business contexts.

---

## 19.1 Person

A Person represents an individual known by an Organization.

A Person exists independently of Meetings.

A Person may participate in:

- zero;
- one;
- many Meetings.

---

## 19.2 Participant

A Participant represents one Person participating in one Meeting.

Every Participant references exactly one Person.

Every Participant belongs to exactly one Meeting.

A Person may therefore generate multiple Participants throughout time.

Each Participant represents one historical participation.

---

## 19.3 Roles

Roles describe responsibilities assumed during one participation.

Examples include:

- Chair;
- Secretary;
- Member;
- Guest;
- Observer;
- Advisor.

Roles belong to Participants.

Roles never belong directly to Persons.

---

## 19.4 Historical Nature

After a Meeting concludes, Participants become part of the permanent historical record.

Their business lifecycle ends.

Their historical existence does not.

Participants therefore remain valid business concepts for:

- auditing;
- traceability;
- historical reconstruction;
- knowledge generation.

---

## 19.5 Participation Principles

### PAR-001

Every Participant references exactly one Person.

---

### PAR-002

Every Participant belongs to exactly one Meeting.

---

### PAR-003

A Person may generate many Participants.

---

### PAR-004

Participants remain historically valid after the Meeting concludes.

---

# 20. Relationships

Relationships express semantic dependencies between business concepts.

Relationships are part of business reality.

They are not implementation artifacts.

---

## 20.1 Relationship Semantics

Relationships may express:

- containment;
- reference;
- association.

Each relationship shall possess explicit business meaning.

---

## 20.2 Business Relationships

The following conceptual relationships exist within the Business Domain.

Organization

contains

Meetings

Meeting

contains

Participants

Meeting

contains

Discussions

Meeting

contains

Business Facts

Participant

references

Person

Motion

belongs to

Discussion

Resolution

addresses

Motion

Action

originates from

Resolution

Business Facts

reference

Business Concepts

---

## 20.3 Relationship Principles

### REL-001

Relationships never redefine business concepts.

---

### REL-002

Relationships preserve business meaning independently of software implementation.

---

### REL-003

Relationships may evolve only if business reality evolves.

---

# 21. Time

Every business concept interacts with time differently.

The ontology distinguishes four temporal behaviors.

---

## Persistent Concepts

Aggregate Roots and Entities evolve throughout time.

Their identity remains stable.

Their attributes may change.

---

## Immutable Concepts

Value Objects are immutable.

Replacing a Value Object creates a new descriptive state.

It never changes the historical value previously associated with a business concept.

---

## Historical Occurrences

Business Facts occur once.

They permanently record objective business reality.

Business Facts never evolve.

Business Facts never disappear.

---

## Relationships

Relationships remain valid as long as the concepts they relate remain valid.

Historical relationships remain part of business history.

---

## Temporal Principles

### TMP-001

Business reality evolves through Business Facts.

---

### TMP-002

Historical information shall never be rewritten.

---

### TMP-003

Every historical state shall remain reconstructable.

---

# 22. Knowledge Domain Boundary

The Knowledge Domain is intentionally excluded from this ontology.

This document defines only the Business Domain.

Nevertheless, the existence of the Knowledge Domain is recognized because it depends conceptually upon Business Facts.

The Knowledge Domain interprets business reality.

It never defines it.

---

## 22.1 Inputs

The Knowledge Domain consumes:

- Business Facts;
- Business Concepts;
- Relationships.

---

## 22.2 Outputs

The Knowledge Domain may produce:

- summaries;
- semantic structures;
- evidence chains;
- inferred topics;
- confidence assessments;
- draft meeting minutes.

These outputs are interpretations.

They are not business reality.

---

## 22.3 Dependency Rule

The dependency between domains is strictly one-way.

Business Domain

↓

Knowledge Domain

The Business Domain shall never depend upon interpretations produced by the Knowledge Domain.

---

## 22.4 Traceability Principle

Every element produced by the Knowledge Domain shall be traceable to one or more Business Facts.

Interpretations without supporting evidence shall not be considered authoritative.

Business Facts remain the ultimate source of truth.

---

# End of Part 3

# 23. Ontological Invariants

The following statements are considered invariant within the current version of this ontology.

They describe properties of business reality rather than software implementation.

Every future design artifact shall remain compatible with these invariants.

---

## INV-001 — Reality Exists Independently

Business reality exists independently of software.

Software observes business reality.

Software never creates business reality.

---

## INV-002 — Objective Occurrences

Business Facts represent objective occurrences.

Business Facts never represent interpretations.

---

## INV-003 — Immutability

Business Facts are immutable.

Historical information shall never be modified.

If reality evolves, new Business Facts shall be created.

---

## INV-004 — Identity

Aggregate Roots and Entities possess persistent identity.

Identity remains stable throughout the business lifecycle.

---

## INV-005 — Descriptive Information

Value Objects possess no identity.

Equivalent Value Objects represent equivalent meaning.

---

## INV-006 — Historical Preservation

Historical business concepts remain part of business reality.

Historical identity is never lost.

---

## INV-007 — Relationships

Relationships express semantic dependencies.

Relationships never redefine the concepts they connect.

---

## INV-008 — Traceability

Every interpretation produced outside the Business Domain shall be traceable to one or more Business Facts.

---

## INV-009 — Separation of Domains

The Business Domain does not depend upon the Knowledge Domain.

The Knowledge Domain depends upon the Business Domain.

---

## INV-010 — Source of Truth

Business Facts constitute the authoritative source of truth for the project.

Interpretations may evolve.

Business Facts do not.

---

# 24. Conceptual Overview

The ontology defines two conceptual domains connected by a unidirectional dependency.

```
                        Business Reality
                               │
                               ▼
                    ┌────────────────────┐
                    │  Business Domain   │
                    └────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
   Aggregate Roots         Entities         Business Facts
          │                    │                    │
          └────────────────────┴────────────────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ Knowledge Domain   │
                    └────────────────────┘
                               │
                               ▼
                    Human-readable Artifacts
```

The diagram represents conceptual dependency only.

It does not represent implementation flow.

---

# 25. Concept Glossary

## Aggregate Root

An autonomous business concept defining the primary boundary of a coherent business context.

---

## Business Domain

The conceptual representation of objective business reality.

---

## Business Fact

An immutable record describing an objective business occurrence.

---

## Entity

A distinguishable business concept possessing persistent identity.

---

## Human-readable Artifact

A document generated for human consumption from interpreted business knowledge.

Examples include meeting minutes, summaries and reports.

Artifacts do not belong to the Business Domain.

---

## Knowledge Domain

The conceptual domain responsible for interpreting Business Facts.

It depends entirely upon the Business Domain.

---

## Meeting

A business event conducted by an Organization.

Meetings constitute the primary context in which Business Facts occur.

---

## Organization

An institution capable of conducting Meetings.

---

## Participant

An Entity representing one Person participating in one Meeting.

---

## Person

An individual known by an Organization.

Persons exist independently of Meetings.

---

## Relationship

A meaningful semantic association between business concepts.

---

## Value Object

Immutable descriptive information without independent identity.

---

# 26. Conformance

Every document belonging to this project shall conform to this ontology.

This includes, but is not limited to:

- Domain Model
- Knowledge Model
- Persistence Model
- Processing Pipeline
- API Specification
- User Interface
- Prompt Specifications

No subsequent document may redefine concepts established by this ontology.

If conceptual evolution becomes necessary, this document shall be revised first.

---

# 27. Versioning Policy

The ontology evolves independently of implementation.

Version numbers follow semantic versioning.

---

## Major Version

A major version introduces conceptual incompatibilities.

Examples include:

- new ontological categories;
- changes in business semantics;
- removal of existing concepts.

---

## Minor Version

A minor version introduces conceptual clarifications without breaking compatibility.

Examples include:

- refined definitions;
- improved terminology;
- additional explanatory material.

---

## Patch Version

A patch version introduces editorial corrections only.

Examples include:

- grammar corrections;
- formatting improvements;
- cross-reference fixes.

---

# 28. Future Documents

The following documents progressively specialize the concepts defined by this ontology.

---

## 03-domain-model.md

Defines the complete business model.

Specifies Aggregate Roots, Entities, Value Objects and Business Facts.

---

## 04-business-facts.md

Defines the complete catalog of Business Facts recognized by the Business Domain.

Specifies the semantics, lifecycle, participants, preconditions and consequences of every Business Fact.

Business Facts constitute the objective bridge between the Business Domain and the Knowledge Domain.

Every interpretation produced by the system shall ultimately be traceable to one or more Business Facts defined in this document.

---

## 05-knowledge-model.md

Defines the conceptual structure of the Knowledge Domain.

Describes semantic interpretation independently of implementation technology.

---

## 06-processing-pipeline.md

Defines how Business Facts are discovered, validated and transformed into knowledge.

---

## 07-persistence-model.md

Defines how Business concepts are represented in persistent storage.

Persistence follows the ontology.

The ontology never follows persistence.

---

## 08-api-design.md

Defines the external interfaces through which the system exposes its capabilities.

Specifies API resources, operations, request and response models, authentication, authorization and integration contracts.

The API Design conforms to the Domain Model and shall not redefine business concepts established by the ontology.

---

# 99-project-context.md

---

# 29. Final Statement

This ontology defines the conceptual foundation of the Intelligent Meeting Minutes Engine.

Its purpose is to establish a stable, technology-independent representation of business reality.

Every subsequent architectural decision shall preserve the concepts defined herein.

Business reality remains the primary source of truth.

Software exists only to observe, represent and interpret that reality.

---

**End of Document**

Version 1.1
Status: Stable
