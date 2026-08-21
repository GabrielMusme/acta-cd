# 20 - Phase 3 Execution Backlog

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

Translate the Phase 3 Processing Pipeline MVP exit gate into executable tasks.

---

# 2. Scope

Phase 3 covers the processing pipeline slice from meeting audio input to validated Business Facts, with restartability and traceability controls.

It includes ingestion, preprocessing, transcription, segmentation, candidate extraction, fact validation, checkpoint/restart and processing logs.

It does not start Phase 4 knowledge derivation or Phase 5 API hardening.

---

# 3. Dependencies

- 00-project-design-handbook.md
- 04-business-facts.md
- 06-processing-pipeline.md
- 10-implementation-plan.md
- 11-mvp-technology-stack.md
- 13-operational-status.md
- 16-sample-data-policy.md
- 21-phase3-prerequisites.md

---

# 4. Working Rules

- Processing modules SHALL remain outside Domain and Business Facts core entities.
- Every stage SHALL emit structured outputs with traceable evidence links.
- Stage execution SHALL be restartable from persisted checkpoints.
- Accepted Business Facts SHALL remain immutable and append-only.
- Every task SHALL include verification tests or executable validation commands.

---

# 5. Phase 3 Tasks

## P3-T01 - Define pipeline contracts and stage boundaries

Goal:

- define typed contracts for stage input/output and traceability envelope.

Deliverables:

- processing schemas for artifacts and stage results;
- stage status model (pending, running, completed, failed, skipped);
- correlation metadata contract (meeting_id, run_id, stage_id, timestamps, evidence_refs).

Acceptance criteria:

- every stage boundary has explicit typed input and output contracts;
- contracts can represent success, recoverable failure and fatal failure;
- contracts do not introduce business-domain ownership drift.

Verification:

- unit tests for schema validation;
- import boundary tests ensuring no framework leakage into domain.

## P3-T02 - Implement checkpoint and restart infrastructure

Goal:

- provide deterministic resume behavior at stage level.

Deliverables:

- checkpoint manager service;
- run manifest and stage checkpoint records;
- restart policy for retry and resume.

Acceptance criteria:

- interrupted pipeline can resume without reprocessing completed stages;
- checkpoint records preserve traceability metadata;
- restart does not overwrite immutable Business Facts already persisted.

Verification:

- integration tests simulating interruption and resume;
- negative test for immutable fact overwrite attempts on resume.

## P3-T03 - Implement ingestion and preprocessing adapters

Goal:

- ingest dataset audio and normalize it for downstream processing.

Deliverables:

- ingestion service reading dataset metadata;
- preprocessing adapter using FFmpeg command wrappers;
- generated preprocessing artifact with provenance metadata.

Acceptance criteria:

- metadata validation fails fast on missing or invalid dataset fields;
- original audio remains unchanged;
- preprocessing output is traceable to original artifact checksum.

Verification:

- tests for metadata validation and path safety;
- command-level test for preprocessing adapter behavior.

## P3-T04 - Implement transcription stage (MVP mandatory path)

Goal:

- convert preprocessed audio into structured transcript segments.

Deliverables:

- transcription adapter around faster-whisper;
- transcript segment model with timestamps;
- confidence and engine metadata capture.

Acceptance criteria:

- transcription output is structured and stage-traceable;
- empty or corrupt audio is handled with deterministic error type;
- MVP run can continue toward extraction on successful transcript generation.

Verification:

- fixture-based tests for transcript schema and error handling;
- smoke run on one short sample meeting.

## P3-T05 - Implement segmentation and evidence normalization

Goal:

- split transcript into analyzable units and normalize evidence references.

Deliverables:

- segmentation service;
- normalized evidence reference format;
- segment lineage mapping transcript -> segment -> candidate.

Acceptance criteria:

- each segment references source transcript span;
- segmentation is deterministic for the same input;
- segment metadata is preserved in checkpoints.

Verification:

- deterministic segmentation tests;
- traceability chain tests for lineage mapping.

## P3-T06 - Implement candidate Business Fact extraction

Goal:

- generate candidate facts mapped to BF catalog categories.

Deliverables:

- extraction service returning candidate facts with evidence refs;
- mapping rules from processing output to BF categories;
- rejection reason model for non-mappable candidates.

Acceptance criteria:

- candidates include category, occurred_at, payload and evidence references;
- unsupported claims are marked as rejected candidates;
- extraction output is independent from persistence layer internals.

Verification:

- unit tests for rule mapping and rejection behavior;
- tests for required candidate fields.

## P3-T07 - Implement fact validation gate integration

Goal:

- validate extracted candidates before Business Fact acceptance.

Deliverables:

- validation orchestration using existing business_facts validators;
- integration with domain fact-linking checks;
- accepted/rejected result envelope.

Acceptance criteria:

- accepted facts satisfy BF-001..BF-005 constraints;
- contradictory or unsupported candidates are rejected with reasons;
- accepted facts keep evidence trace links.

Verification:

- integration tests for acceptance/rejection matrix;
- contradiction-focused negative tests.

## P3-T08 - Implement diarization stage with graceful degradation

Goal:

- add speaker attribution support without blocking MVP flow.

Deliverables:

- diarization adapter boundary;
- optional diarization enrichments for transcript/segments;
- fallback behavior when diarization model is unavailable.

Acceptance criteria:

- pipeline continues when diarization is unavailable and marks stage as skipped/degraded;
- diarization labels remain processing artifacts and do not redefine Participant identity;
- diarization outputs are traceable when present.

Verification:

- tests for degraded mode;
- integration test for optional speaker-attributed segments.

## P3-T09 - Build processing orchestrator and structured logs

Goal:

- coordinate stages end-to-end with correlation metadata.

Deliverables:

- pipeline orchestrator service;
- stage execution graph and ordering controls;
- structured logs with run_id and stage context.

Acceptance criteria:

- orchestrator executes MVP path in documented order;
- retries and resume policy integrate with checkpoints;
- logs enable evidence-based troubleshooting by stage.

Verification:

- orchestrator flow tests with stage stubs and real adapters mix;
- simulated stage failure and resume test.

## P3-T10 - Execute first end-to-end local sample run and evidence package

Goal:

- close Phase 3 with executable evidence for the gate.

Deliverables:

- one full local run from sample audio to validated facts;
- execution report under docs/reports/;
- updated operational status and traceability records.

Acceptance criteria:

- pipeline resume after controlled interruption is demonstrated;
- accepted facts are traceable to evidence artifacts;
- invalid candidates are rejected;
- run completes with reproducible commands.

Verification:

- run phase subset tests and smoke test command set;
- attach run summary with timestamps, outputs and known limitations.

---

# 6. Task Dependencies

- P3-T01 before all implementation tasks.
- P3-T02 before P3-T09 and P3-T10.
- P3-T03 before P3-T04.
- P3-T04 before P3-T05.
- P3-T05 before P3-T06.
- P3-T06 before P3-T07.
- P3-T07 and P3-T08 before P3-T09.
- P3-T09 before P3-T10.

---

# 7. Incremental Closure Strategy

- Minimal MVP slice for first integration: P3-T01 to P3-T07 plus P3-T09.
- Speaker enrichment slice: P3-T08 integrated behind optional/degraded mode.
- Gate evidence slice: P3-T10 after stable restart and validation behavior.

---

# 8. Phase 3 Exit Gate

Phase 3 can close only when:

- pipeline can resume after controlled interruption;
- accepted facts are traceable to evidence;
- unsupported or hallucinated candidates are rejected;
- at least one local sample run completes successfully.

---

# 9. Risks and Controls

- Heavy CPU runtime for transcription/diarization: apply short sample fixture first, then medium sample.
- External model download bottlenecks: pre-stage model assets and document cache paths.
- Audio quality variance: keep deterministic fixture set with known expected outputs.
- Boundary drift into domain models: enforce package-level import tests.

---

# 10. Changelog

## 1.0.0

- Created Phase 3 Processing Pipeline MVP backlog with task IDs P3-T01..P3-T10.
- Added dependency graph, incremental closure strategy and gate-aligned acceptance criteria.
