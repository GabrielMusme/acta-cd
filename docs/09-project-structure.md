# 09 - Project Structure and Implementation Modules

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
- 08-api-design.md

---

# 1. Purpose

This document proposes a practical project structure and the main implementation modules for the system.

Its purpose is to translate the design documents into a modular and maintainable codebase while preserving the separation between Business Domain, Knowledge Domain and Processing Domain.

---

# 2. Principles

The implementation structure SHALL follow these rules:

- Business Domain concepts SHALL remain independent from processing implementation.
- Processing modules SHALL not leak technical concepts into the domain model.
- Knowledge modules SHALL depend on the Business Domain and Business Facts, not vice versa.
- The project SHALL be organized around clear responsibilities and bounded modules.

---

# 3. Proposed Repository Structure

```text
project-root/
├── docs/
│   ├── 00-project-design-handbook.md
│   ├── 01-domain-discovery.md
│   ├── 02-domain-ontology.md
│   ├── 03-domain-model.md
│   ├── 04-business-facts.md
│   ├── 05-knowledge-model.md
│   ├── 06-processing-pipeline.md
│   ├── 07-persistence-model.md
│   ├── 08-api-design.md
│   └── 09-project-structure.md
├── src/
│   ├── app/
│   │   ├── main.py
│   │   ├── config/
│   │   ├── dependencies/
│   │   └── routers/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── events/
│   │   ├── repositories/
│   │   └── services/
│   ├── business_facts/
│   │   ├── models/
│   │   ├── services/
│   │   └── validators/
│   ├── knowledge/
│   │   ├── models/
│   │   ├── services/
│   │   ├── evaluators/
│   │   └── exporters/
│   ├── processing/
│   │   ├── ingestion/
│   │   ├── transcription/
│   │   ├── diarization/
│   │   ├── segmentation/
│   │   ├── extraction/
│   │   ├── validation/
│   │   ├── checkpoints/
│   │   └── workers/
│   ├── infrastructure/
│   │   ├── persistence/
│   │   ├── repositories/
│   │   ├── storage/
│   │   └── logging/
│   └── shared/
│       ├── schemas/
│       ├── utils/
│       └── errors/
├── tests/
│   ├── domain/
│   ├── business_facts/
│   ├── knowledge/
│   ├── processing/
│   └── api/
├── data/
│   └── meetings/
├── scripts/
└── pyproject.toml
```

---

# 4. Module Responsibilities

## 4.1 App Layer

Purpose:

- wire dependencies;
- expose the API entrypoints;
- coordinate request handling.

Main modules:

- app.main
- app.routers
- app.dependencies
- app.config

## 4.2 Domain Layer

Purpose:

- contain the Business Domain model;
- define entities, value objects and domain rules;
- remain independent from databases and processing details.

Main modules:

- domain.entities
- domain.value_objects
- domain.events
- domain.repositories
- domain.services

## 4.3 Business Facts Layer

Purpose:

- define the fact model and validation rules;
- ensure facts are immutable and traceable.

Main modules:

- business_facts.models
- business_facts.services
- business_facts.validators

## 4.4 Knowledge Layer

Purpose:

- derive knowledge from Business Facts;
- create summaries, detected topics, decisions, deadlines and evidence.

Main modules:

- knowledge.models
- knowledge.services
- knowledge.evaluators
- knowledge.exporters

## 4.5 Processing Layer

Purpose:

- implement the pipeline stages;
- ingest raw audio and produce validated facts and knowledge outputs.

Main modules:

- processing.ingestion
- processing.transcription
- processing.diarization
- processing.segmentation
- processing.extraction
- processing.validation
- processing.checkpoints
- processing.workers

## 4.6 Infrastructure Layer

Purpose:

- implement persistence, storage, logging and external integrations.

Main modules:

- infrastructure.persistence
- infrastructure.repositories
- infrastructure.storage
- infrastructure.logging

## 4.7 Shared Layer

Purpose:

- hold cross-cutting helpers, schemas and errors.

Main modules:

- shared.schemas
- shared.utils
- shared.errors

---

# 5. Suggested Dependencies Between Modules

The dependency direction SHOULD be:

```text
app -> domain -> business_facts -> knowledge -> processing -> infrastructure
```

With the following rules:

- domain SHALL NOT depend on processing.
- knowledge SHALL depend on domain and business_facts.
- processing SHALL depend on domain, business_facts and knowledge concepts as needed.
- infrastructure SHALL implement interfaces defined by higher layers.

---

# 6. Module Interaction Example

A typical flow could be:

1. App starts a processing job for a meeting.
2. Processing ingests audio.
3. Processing produces intermediate evidence and candidate facts.
4. Business facts service validates candidates.
5. Domain entities are updated or linked to the validated facts.
6. Knowledge services derive summaries and other outputs from the validated facts.
7. Infrastructure persists the results and exposes them via the API.

---

# 7. Testing Structure

Tests SHOULD be organized to mirror the module structure.

Suggested folders:

- tests/domain
- tests/business_facts
- tests/knowledge
- tests/processing
- tests/api

Recommended test types:

- unit tests for validators and services;
- integration tests for persistence and API routes;
- end-to-end tests for the processing pipeline where feasible.

---

# 8. Implementation Notes

## 8.1 Layering

The project SHOULD maintain a clear layering model:

- interface layer: routers and API contracts;
- application layer: orchestration and use cases;
- domain layer: business concepts and rules;
- infrastructure layer: persistence and external systems.

## 8.2 Dependency Inversion

Repositories and adapters SHOULD be defined through interfaces in the higher layers.

Infrastructure implementations SHOULD satisfy those interfaces.

## 8.3 Reusability

Shared utilities SHOULD remain generic and not depend on the domain model directly.

---

# 9. Open Questions

The following questions remain open for implementation planning.

- Should the project use a monolithic structure first or a package-based modular layout?
- Should the API and processing services be deployed as separate processes from the start?
- Should the first implementation target the full pipeline or a minimal vertical slice?

---

# 10. Future Improvements

- Define a concrete package naming convention for Python modules.
- Add a dependency graph and architecture rules.
- Split the processing layer into separate worker packages if the pipeline grows.
- Add a deployment structure for local/offline execution.

---

# 11. Changelog

## 1.0.0

- Created the initial project structure and module proposal.
- Aligned the proposal with the Business Domain, Knowledge Domain, Processing Domain and persistence/API design.
