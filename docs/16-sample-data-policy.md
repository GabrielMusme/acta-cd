# 16 - Sample Data Policy

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Active

---

# 1. Purpose

Define safe and reproducible sample input rules for MVP validation runs.

---

# 2. Scope

This policy governs sample meeting assets stored under data/meetings and used in local and CI-adjacent validation.

---

# 3. Dependencies

- 00-project-design-handbook.md
- 06-processing-pipeline.md
- 10-implementation-plan.md
- 12-mvp-execution-backlog.md

---

# 4. Definitions

- Sample dataset: controlled set of files representing one meeting input and its metadata.
- Metadata file: structured descriptor of origin, license and integrity for a dataset.
- Local-only processing: execution performed offline on project-controlled infrastructure.

---

# 5. Requirements

- Sample assets SHALL follow offline execution constraints (ARCH-001).
- Original audio files SHALL remain immutable (ARCH-002).
- Every sample dataset SHALL include structured metadata for traceability.
- Sample assets SHALL use permissive licensing or explicit internal authorization for local project use.
- No sample data SHALL require cloud-hosted access tokens for retrieval or processing.

---

# 6. Design

## 6.1 Storage and Naming Conventions

Each dataset uses one dedicated folder under data/meetings with this pattern:

- meeting_<sequence>_<yyyy-mm-dd>_<slug>

Example:

- meeting_000001_2026-08-15_governance-sync

Required internal layout:

- original/
- audio/
- segments/
- knowledge/
- output/
- logs/
- metadata.yaml

This layout is aligned with storage conventions from the project design handbook.

## 6.2 Metadata Requirements

Each metadata.yaml SHALL include at least:

- dataset_id
- meeting_id
- created_at_utc
- source_type
- language
- duration_seconds
- audio_format
- license
- license_evidence
- contains_pii
- consent_reference
- sha256_original_audio
- storage_root
- notes

Reference template:

- data/meetings/metadata-template.yaml

## 6.3 Licensing and Privacy Rules

- Allowed by default: CC0, CC-BY 4.0, or organization-owned recordings with documented authorization.
- Not allowed: assets with unclear ownership, restrictive redistribution terms, or unknown provenance.
- If contains_pii is true, metadata SHALL include a consent_reference and usage scope note.

## 6.4 Verification Checklist Review (Simulated)

Reviewed dataset:

- data/meetings/meeting_000000_1970-01-01_template

Review result:

- Folder naming rule: pass
- Required subfolders present: pass
- metadata.yaml present: pass
- License fields present: pass
- Offline/local usage compatibility: pass

---

# 7. Diagrams

No diagram required.

---

# 8. Data Models

Metadata schema shape is represented by data/meetings/metadata-template.yaml.

---

# 9. Interfaces

The processing ingestion stage reads dataset metadata before any pipeline execution.

---

# 10. Error Handling

- Missing metadata.yaml: dataset is rejected.
- Missing license fields: dataset is rejected.
- Hash mismatch on original audio: dataset is quarantined for manual review.

---

# 11. Future Improvements

- Add automated metadata validation in pre-processing checks.
- Add optional anonymization policy for published fixtures.

---

# 12. Changelog

## 1.0.0

- Created sample data policy for P0-T06.
