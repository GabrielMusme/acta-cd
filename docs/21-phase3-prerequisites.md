# 21 - Phase 3 Prerequisites

**Project:** Intelligent Meeting Minutes Engine

**Version:** 1.0

**Status:** Active

---

# 1. Purpose

Define the local prerequisites and operator intervention points before implementing and validating Phase 3 processing.

---

# 2. Dependencies

- 06-processing-pipeline.md
- 10-implementation-plan.md
- 11-mvp-technology-stack.md
- 16-sample-data-policy.md
- 20-phase3-execution-backlog.md

---

# 3. Prerequisite Checklist

## 3.1 Runtime and Tooling

- [x] Python 3.12 target available.
- [x] uv environment and lock workflow available.
- [x] pytest and Ruff quality gate available.
- [ ] FFmpeg binary available in PATH.
- [ ] Processing dependencies for transcription and diarization added and locked.

## 3.2 Processing Dependencies (MVP)

- [ ] faster-whisper dependency installed and importable.
- [ ] ctranslate2 runtime installed and compatible with CPU execution.
- [ ] pyannote.audio dependency installed and importable.
- [ ] torch CPU runtime compatible with selected pyannote version.
- [ ] spaCy baseline package installed for normalization support.

## 3.3 Model Assets and Cache Strategy

- [ ] transcription model size policy selected for MVP fixture runs.
- [ ] local model cache path documented for reproducible runs.
- [ ] diarization model acquisition path defined.
- [ ] degraded mode policy approved when diarization model is not locally available.

## 3.4 Sample Audio and Metadata

- [ ] at least one local sample dataset exists under data/meetings/ with required folder layout.
- [ ] metadata.yaml completed from template with license and provenance fields.
- [ ] original audio checksum recorded in metadata.
- [ ] sample fixture duration for first MVP run is between 2 and 10 minutes.

## 3.5 Environment Contract

Required variables for Phase 3 runs:

- `ACTA_DATABASE_URL`
- `ACTA_TEST_DATABASE_URL`
- `ACTA_MEETINGS_ROOT` (default: data/meetings)
- `ACTA_MODELS_CACHE_DIR`
- `ACTA_PIPELINE_RUNS_DIR`

Optional variable when external model download is needed:

- `HF_TOKEN` (only for model bootstrap, never committed).

---

# 4. Operator Intervention Points

The following items may require explicit operator action before coding can proceed:

1. Install system-level FFmpeg packages if unavailable in the environment.
2. Confirm whether model downloads from external registries are allowed during bootstrap.
3. Provide one approved sample audio dataset with completed metadata and license evidence.
4. Confirm maximum acceptable local runtime for first smoke run (suggested target: <= 20 minutes).

---

# 5. Verification Sequence

1. Run `uv sync --dev` and confirm clean environment.
2. Verify FFmpeg availability with `ffmpeg -version`.
3. Install and verify processing dependencies with import smoke checks.
4. Prepare sample dataset folder and metadata under data/meetings/.
5. Configure required environment variables.
6. Run MVP dry pipeline with stage stubs (no heavy models).
7. Run MVP real transcription path on short audio.
8. Enable diarization stage and verify degraded fallback behavior.

---

# 6. Go/No-Go Criteria for Starting P3-T03

Go only when all are true:

- FFmpeg is available locally.
- One sample dataset is available and policy-compliant.
- Transcription dependency imports pass.
- Checkpoint output directory permissions are verified.

No-Go conditions:

- missing sample audio or invalid license/provenance metadata;
- missing FFmpeg binary;
- unresolved dependency conflicts for transcription runtime.

---

# 7. Error Handling

- Missing FFmpeg: block preprocessing implementation and tests.
- Missing sample dataset: block end-to-end and smoke validation.
- Model bootstrap failure: keep diarization in degraded mode and continue non-diarized MVP slice.
- Runtime too slow for local loop: reduce fixture duration and transcription model size.

---

# 8. Changelog

## 1.0.0

- Created Phase 3 prerequisite checklist with explicit operator intervention points.
- Added runtime, dependency, model, dataset and environment readiness gates for Phase 3.
