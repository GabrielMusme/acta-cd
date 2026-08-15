"""Business Fact domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Mapping


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


class BusinessFactCategory(str, Enum):
    BF_001_MEETING_CREATED = "BF-001"
    BF_002_MEETING_STARTED = "BF-002"
    BF_003_MEETING_CLOSED = "BF-003"
    BF_004_PARTICIPANT_JOINED = "BF-004"
    BF_005_PARTICIPANT_LEFT = "BF-005"
    BF_006_AGENDA_LOADED = "BF-006"
    BF_007_DISCUSSION_STARTED = "BF-007"
    BF_008_DISCUSSION_CLOSED = "BF-008"
    BF_009_MOTION_PROPOSED = "BF-009"
    BF_010_MOTION_AMENDED = "BF-010"
    BF_011_MOTION_WITHDRAWN = "BF-011"
    BF_012_VOTE_STARTED = "BF-012"
    BF_013_VOTE_CLOSED = "BF-013"
    BF_014_RESOLUTION_APPROVED = "BF-014"
    BF_015_RESOLUTION_REJECTED = "BF-015"
    BF_016_ACTION_ASSIGNED = "BF-016"
    BF_017_ACTION_COMPLETED = "BF-017"
    BF_018_DOCUMENT_REFERENCED = "BF-018"


@dataclass(frozen=True, slots=True)
class ConceptReference:
    concept_type: str
    concept_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "concept_type", _require_non_empty(self.concept_type, "concept_type")
        )
        object.__setattr__(self, "concept_id", _require_non_empty(self.concept_id, "concept_id"))


@dataclass(frozen=True, slots=True)
class BusinessFact:
    fact_id: str
    category: BusinessFactCategory
    meeting_id: str
    occurred_at: datetime
    references: tuple[ConceptReference, ...]
    payload: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "fact_id", _require_non_empty(self.fact_id, "fact_id"))
        object.__setattr__(self, "meeting_id", _require_non_empty(self.meeting_id, "meeting_id"))

        if not isinstance(self.category, BusinessFactCategory):
            raise ValueError("category must be a BusinessFactCategory")

        if not isinstance(self.occurred_at, datetime):
            raise ValueError("occurred_at must be a datetime")

        refs = tuple(self.references)
        if not refs:
            raise ValueError("references must contain one or more ConceptReference")
        if not all(isinstance(reference, ConceptReference) for reference in refs):
            raise ValueError("references must contain only ConceptReference values")
        object.__setattr__(self, "references", refs)

        payload_dict = dict(self.payload)
        object.__setattr__(self, "payload", MappingProxyType(payload_dict))


@dataclass(frozen=True, slots=True)
class BusinessFactLog:
    """Append-only ledger of immutable Business Facts."""

    facts: tuple[BusinessFact, ...] = ()

    def append(self, fact: BusinessFact) -> BusinessFactLog:
        if not isinstance(fact, BusinessFact):
            raise ValueError("fact must be a BusinessFact")
        return BusinessFactLog(facts=self.facts + (fact,))
