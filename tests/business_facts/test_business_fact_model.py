from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from business_facts.models import (
    BusinessFact,
    BusinessFactCategory,
    BusinessFactLog,
    ConceptReference,
)

pytestmark = [pytest.mark.phase1_gate, pytest.mark.phase1_fact_immutability]


def _reference() -> ConceptReference:
    return ConceptReference(concept_type="Meeting", concept_id="meeting-1")


def _fact() -> BusinessFact:
    return BusinessFact(
        fact_id="fact-1",
        category=BusinessFactCategory.BF_001_MEETING_CREATED,
        meeting_id="meeting-1",
        occurred_at=datetime(2026, 8, 15, 10, 0, 0),
        references=(_reference(),),
        payload={"source": "unit-test"},
    )


def test_business_fact_category_catalog_covers_bf_001_to_bf_018() -> None:
    assert len(BusinessFactCategory) == 18
    assert BusinessFactCategory.BF_001_MEETING_CREATED.value == "BF-001"
    assert BusinessFactCategory.BF_018_DOCUMENT_REFERENCED.value == "BF-018"


def test_business_fact_is_immutable_and_has_explicit_references() -> None:
    fact = _fact()
    assert fact.references[0].concept_type == "Meeting"

    with pytest.raises(FrozenInstanceError):
        fact.meeting_id = "meeting-2"  # type: ignore[misc]


def test_business_fact_requires_meeting_reference() -> None:
    with pytest.raises(ValueError):
        BusinessFact(
            fact_id="fact-1",
            category=BusinessFactCategory.BF_001_MEETING_CREATED,
            meeting_id=" ",
            occurred_at=datetime(2026, 8, 15, 10, 0, 0),
            references=(_reference(),),
        )


def test_business_fact_requires_one_or_more_concept_references() -> None:
    with pytest.raises(ValueError):
        BusinessFact(
            fact_id="fact-1",
            category=BusinessFactCategory.BF_001_MEETING_CREATED,
            meeting_id="meeting-1",
            occurred_at=datetime(2026, 8, 15, 10, 0, 0),
            references=(),
        )


def test_business_fact_references_must_be_typed() -> None:
    with pytest.raises(ValueError):
        BusinessFact(
            fact_id="fact-1",
            category=BusinessFactCategory.BF_001_MEETING_CREATED,
            meeting_id="meeting-1",
            occurred_at=datetime(2026, 8, 15, 10, 0, 0),
            references=("meeting-1",),  # type: ignore[arg-type]
        )


def test_business_fact_payload_is_immutable_mapping() -> None:
    fact = _fact()

    with pytest.raises(TypeError):
        fact.payload["another"] = "value"  # type: ignore[index]


def test_business_fact_log_is_append_only() -> None:
    initial_log = BusinessFactLog()
    first_fact = _fact()

    updated_log = initial_log.append(first_fact)

    assert initial_log.facts == ()
    assert len(updated_log.facts) == 1
    assert updated_log.facts[0] == first_fact


def test_business_fact_log_rejects_invalid_entries() -> None:
    with pytest.raises(ValueError):
        BusinessFactLog().append("not-a-fact")  # type: ignore[arg-type]
