from datetime import datetime

import pytest

from business_facts.models import (
    BusinessFact,
    BusinessFactCategory,
    BusinessFactLog,
    ConceptReference,
)
from business_facts.validators import BusinessFactValidator

pytestmark = [pytest.mark.phase1_gate]


def _fact(
    *,
    fact_id: str,
    category: BusinessFactCategory,
    meeting_id: str = "meeting-1",
    references: tuple[ConceptReference, ...],
    payload: dict[str, object] | None = None,
) -> BusinessFact:
    return BusinessFact(
        fact_id=fact_id,
        category=category,
        meeting_id=meeting_id,
        occurred_at=datetime(2026, 8, 16, 10, 0, 0),
        references=references,
        payload=payload or {},
    )


def _known_concepts() -> set[tuple[str, str]]:
    return {
        ("Organization", "org-1"),
        ("Meeting", "meeting-1"),
        ("Participant", "participant-1"),
        ("Person", "person-1"),
        ("Agenda", "agenda-1"),
        ("AgendaItem", "agenda-item-1"),
        ("Discussion", "discussion-1"),
        ("Motion", "motion-1"),
        ("Vote", "vote-1"),
        ("Resolution", "resolution-1"),
        ("Action", "action-1"),
        ("Attachment", "attachment-1"),
    }


def test_acceptance_rejection_matrix_for_required_references_and_known_concepts() -> None:
    validator = BusinessFactValidator()
    known = _known_concepts()

    valid = _fact(
        fact_id="fact-1",
        category=BusinessFactCategory.BF_004_PARTICIPANT_JOINED,
        references=(
            ConceptReference("Participant", "participant-1"),
            ConceptReference("Meeting", "meeting-1"),
            ConceptReference("Person", "person-1"),
        ),
    )
    valid_result = validator.validate(valid, history=BusinessFactLog(), known_concepts=known)
    assert valid_result.accepted

    missing_ref = _fact(
        fact_id="fact-2",
        category=BusinessFactCategory.BF_004_PARTICIPANT_JOINED,
        references=(
            ConceptReference("Participant", "participant-1"),
            ConceptReference("Meeting", "meeting-1"),
        ),
    )
    missing_ref_result = validator.validate(
        missing_ref,
        history=BusinessFactLog(),
        known_concepts=known,
    )
    assert not missing_ref_result.accepted
    assert missing_ref_result.errors[0].reason == "missing_required_references"

    unknown_ref = _fact(
        fact_id="fact-3",
        category=BusinessFactCategory.BF_006_AGENDA_LOADED,
        references=(
            ConceptReference("Meeting", "meeting-1"),
            ConceptReference("Agenda", "agenda-does-not-exist"),
        ),
    )
    unknown_ref_result = validator.validate(
        unknown_ref,
        history=BusinessFactLog(),
        known_concepts=known,
    )
    assert not unknown_ref_result.accepted
    assert unknown_ref_result.errors[0].reason == "unknown_concept_reference"


def test_unsupported_category_is_rejected() -> None:
    validator = BusinessFactValidator(
        supported_categories={
            BusinessFactCategory.BF_001_MEETING_CREATED,
            BusinessFactCategory.BF_002_MEETING_STARTED,
        }
    )
    candidate = _fact(
        fact_id="fact-unsupported",
        category=BusinessFactCategory.BF_018_DOCUMENT_REFERENCED,
        references=(
            ConceptReference("Attachment", "attachment-1"),
            ConceptReference("Meeting", "meeting-1"),
        ),
    )

    result = validator.validate(
        candidate, history=BusinessFactLog(), known_concepts=_known_concepts()
    )
    assert not result.accepted
    assert result.errors[0].reason == "unsupported_fact_category"


def test_contradiction_requires_corrective_fact_flow() -> None:
    validator = BusinessFactValidator()
    history = BusinessFactLog().append(
        _fact(
            fact_id="fact-withdrawn",
            category=BusinessFactCategory.BF_011_MOTION_WITHDRAWN,
            references=(
                ConceptReference("Motion", "motion-1"),
                ConceptReference("Discussion", "discussion-1"),
            ),
        )
    )

    contradictory = _fact(
        fact_id="fact-amended",
        category=BusinessFactCategory.BF_010_MOTION_AMENDED,
        references=(
            ConceptReference("Motion", "motion-1"),
            ConceptReference("Discussion", "discussion-1"),
        ),
    )
    result = validator.validate(contradictory, history=history, known_concepts=_known_concepts())
    assert not result.accepted
    assert result.errors[0].reason == "contradictory_immutable_history"

    corrective = _fact(
        fact_id="fact-amended-corrective",
        category=BusinessFactCategory.BF_010_MOTION_AMENDED,
        references=(
            ConceptReference("Motion", "motion-1"),
            ConceptReference("Discussion", "discussion-1"),
        ),
        payload={"corrective_for": "fact-withdrawn"},
    )
    corrective_result = validator.validate(
        corrective,
        history=history,
        known_concepts=_known_concepts(),
    )
    assert corrective_result.accepted


def test_negative_contradiction_cases_for_history_rules() -> None:
    validator = BusinessFactValidator()

    left_without_join = _fact(
        fact_id="fact-left",
        category=BusinessFactCategory.BF_005_PARTICIPANT_LEFT,
        references=(
            ConceptReference("Participant", "participant-1"),
            ConceptReference("Meeting", "meeting-1"),
        ),
    )
    result_left = validator.validate(
        left_without_join,
        history=BusinessFactLog(),
        known_concepts=_known_concepts(),
    )
    assert not result_left.accepted
    assert result_left.errors[0].reason == "contradictory_immutable_history"

    closed_meeting_history = BusinessFactLog().append(
        _fact(
            fact_id="fact-closed",
            category=BusinessFactCategory.BF_003_MEETING_CLOSED,
            references=(ConceptReference("Meeting", "meeting-1"),),
        )
    )
    start_after_close = _fact(
        fact_id="fact-started",
        category=BusinessFactCategory.BF_002_MEETING_STARTED,
        references=(ConceptReference("Meeting", "meeting-1"),),
    )
    result_start = validator.validate(
        start_after_close,
        history=closed_meeting_history,
        known_concepts=_known_concepts(),
    )
    assert not result_start.accepted
    assert result_start.errors[0].reason == "contradictory_immutable_history"


def test_validation_errors_include_traceable_reason_fields() -> None:
    validator = BusinessFactValidator()
    candidate = _fact(
        fact_id="fact-bad",
        category=BusinessFactCategory.BF_006_AGENDA_LOADED,
        references=(ConceptReference("Meeting", "meeting-1"),),
    )

    result = validator.validate(
        candidate, history=BusinessFactLog(), known_concepts=_known_concepts()
    )
    assert not result.accepted
    error = result.errors[0]

    assert error.code.startswith("BFV-")
    assert error.rule_id in {"BF-001", "BF-002", "BF-004"}
    assert error.fact_id == "fact-bad"
    assert error.reason
    assert error.details


def test_validate_batch_returns_acceptance_and_rejection_rows() -> None:
    validator = BusinessFactValidator()
    known = _known_concepts()
    candidates = (
        _fact(
            fact_id="fact-ok-1",
            category=BusinessFactCategory.BF_001_MEETING_CREATED,
            references=(
                ConceptReference("Organization", "org-1"),
                ConceptReference("Meeting", "meeting-1"),
            ),
        ),
        _fact(
            fact_id="fact-bad-1",
            category=BusinessFactCategory.BF_004_PARTICIPANT_JOINED,
            references=(ConceptReference("Participant", "participant-1"),),
        ),
    )

    batch = validator.validate_batch(candidates, history=BusinessFactLog(), known_concepts=known)

    assert len(batch.accepted_facts) == 1
    assert batch.accepted_facts[0].fact_id == "fact-ok-1"
    assert len(batch.accepted_log.facts) == 1
    assert len(batch.rejected) == 1
    assert batch.rejected[0][0].fact_id == "fact-bad-1"
