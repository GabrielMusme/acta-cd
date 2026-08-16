"""Business Fact validation pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from business_facts.models import (
    BusinessFact,
    BusinessFactCategory,
    BusinessFactLog,
)

ConceptKey = tuple[str, str]


@dataclass(frozen=True, slots=True)
class FactValidationError:
    code: str
    rule_id: str
    reason: str
    fact_id: str
    details: str


@dataclass(frozen=True, slots=True)
class FactValidationResult:
    accepted: bool
    errors: tuple[FactValidationError, ...] = ()


@dataclass(frozen=True, slots=True)
class FactValidationBatchResult:
    accepted_log: BusinessFactLog
    accepted_facts: tuple[BusinessFact, ...]
    rejected: tuple[tuple[BusinessFact, tuple[FactValidationError, ...]], ...]


_REQUIRED_CONCEPT_TYPES: dict[BusinessFactCategory, frozenset[str]] = {
    BusinessFactCategory.BF_001_MEETING_CREATED: frozenset({"Organization", "Meeting"}),
    BusinessFactCategory.BF_002_MEETING_STARTED: frozenset({"Meeting"}),
    BusinessFactCategory.BF_003_MEETING_CLOSED: frozenset({"Meeting"}),
    BusinessFactCategory.BF_004_PARTICIPANT_JOINED: frozenset({"Participant", "Meeting", "Person"}),
    BusinessFactCategory.BF_005_PARTICIPANT_LEFT: frozenset({"Participant", "Meeting"}),
    BusinessFactCategory.BF_006_AGENDA_LOADED: frozenset({"Meeting", "Agenda"}),
    BusinessFactCategory.BF_007_DISCUSSION_STARTED: frozenset(
        {"Discussion", "Meeting", "AgendaItem"}
    ),
    BusinessFactCategory.BF_008_DISCUSSION_CLOSED: frozenset({"Discussion", "Meeting"}),
    BusinessFactCategory.BF_009_MOTION_PROPOSED: frozenset({"Motion", "Discussion"}),
    BusinessFactCategory.BF_010_MOTION_AMENDED: frozenset({"Motion", "Discussion"}),
    BusinessFactCategory.BF_011_MOTION_WITHDRAWN: frozenset({"Motion", "Discussion"}),
    BusinessFactCategory.BF_012_VOTE_STARTED: frozenset({"Vote", "Motion"}),
    BusinessFactCategory.BF_013_VOTE_CLOSED: frozenset({"Vote", "Motion"}),
    BusinessFactCategory.BF_014_RESOLUTION_APPROVED: frozenset({"Resolution", "Motion"}),
    BusinessFactCategory.BF_015_RESOLUTION_REJECTED: frozenset({"Resolution", "Motion"}),
    BusinessFactCategory.BF_016_ACTION_ASSIGNED: frozenset({"Action", "Resolution"}),
    BusinessFactCategory.BF_017_ACTION_COMPLETED: frozenset({"Action", "Resolution"}),
    BusinessFactCategory.BF_018_DOCUMENT_REFERENCED: frozenset({"Attachment", "Meeting"}),
}


class BusinessFactValidator:
    """Validates Business Facts against catalog and immutable history rules."""

    def __init__(self, supported_categories: set[BusinessFactCategory] | None = None) -> None:
        self._supported_categories = supported_categories or set(BusinessFactCategory)

    def validate(
        self,
        candidate: BusinessFact,
        *,
        history: BusinessFactLog,
        known_concepts: set[ConceptKey] | None = None,
    ) -> FactValidationResult:
        errors: list[FactValidationError] = []

        if candidate.category not in self._supported_categories:
            errors.append(
                FactValidationError(
                    code="BFV-001",
                    rule_id="BF-001",
                    reason="unsupported_fact_category",
                    fact_id=candidate.fact_id,
                    details=(
                        f"Category {candidate.category.value} is not enabled in this validator."
                    ),
                )
            )
            return FactValidationResult(accepted=False, errors=tuple(errors))

        required_types = _REQUIRED_CONCEPT_TYPES[candidate.category]
        present_types = {reference.concept_type for reference in candidate.references}
        missing_types = sorted(required_types - present_types)
        if missing_types:
            errors.append(
                FactValidationError(
                    code="BFV-002",
                    rule_id="BF-004",
                    reason="missing_required_references",
                    fact_id=candidate.fact_id,
                    details=f"Missing required concept types: {', '.join(missing_types)}",
                )
            )

        if known_concepts is not None:
            missing_concepts = [
                (reference.concept_type, reference.concept_id)
                for reference in candidate.references
                if (reference.concept_type, reference.concept_id) not in known_concepts
            ]
            if missing_concepts:
                errors.append(
                    FactValidationError(
                        code="BFV-003",
                        rule_id="BF-004",
                        reason="unknown_concept_reference",
                        fact_id=candidate.fact_id,
                        details=f"Unknown concept references: {missing_concepts}",
                    )
                )

        contradiction_reason = self._find_contradiction(candidate, history)
        if contradiction_reason and not self._is_corrective(candidate):
            errors.append(
                FactValidationError(
                    code="BFV-004",
                    rule_id="BF-002",
                    reason="contradictory_immutable_history",
                    fact_id=candidate.fact_id,
                    details=contradiction_reason,
                )
            )

        return FactValidationResult(accepted=not errors, errors=tuple(errors))

    def validate_batch(
        self,
        candidates: Iterable[BusinessFact],
        *,
        history: BusinessFactLog,
        known_concepts: set[ConceptKey] | None = None,
    ) -> FactValidationBatchResult:
        accepted_log = history
        accepted_facts: list[BusinessFact] = []
        rejected: list[tuple[BusinessFact, tuple[FactValidationError, ...]]] = []

        for candidate in candidates:
            result = self.validate(candidate, history=accepted_log, known_concepts=known_concepts)
            if result.accepted:
                accepted_log = accepted_log.append(candidate)
                accepted_facts.append(candidate)
            else:
                rejected.append((candidate, result.errors))

        return FactValidationBatchResult(
            accepted_log=accepted_log,
            accepted_facts=tuple(accepted_facts),
            rejected=tuple(rejected),
        )

    @staticmethod
    def _is_corrective(candidate: BusinessFact) -> bool:
        corrective_for = candidate.payload.get("corrective_for")
        return isinstance(corrective_for, str) and bool(corrective_for.strip())

    def _find_contradiction(self, candidate: BusinessFact, history: BusinessFactLog) -> str | None:
        if candidate.category == BusinessFactCategory.BF_002_MEETING_STARTED and self._has_category(
            history, BusinessFactCategory.BF_003_MEETING_CLOSED, meeting_id=candidate.meeting_id
        ):
            return "Meeting cannot be started after a meeting-closed fact exists."

        if candidate.category == BusinessFactCategory.BF_003_MEETING_CLOSED and self._has_category(
            history, BusinessFactCategory.BF_003_MEETING_CLOSED, meeting_id=candidate.meeting_id
        ):
            return "Meeting cannot be closed more than once in immutable history."

        if candidate.category == BusinessFactCategory.BF_005_PARTICIPANT_LEFT:
            participant_id = self._reference_id(candidate, "Participant")
            if participant_id and not self._has_category_with_reference(
                history,
                BusinessFactCategory.BF_004_PARTICIPANT_JOINED,
                "Participant",
                participant_id,
                meeting_id=candidate.meeting_id,
            ):
                return "Participant cannot leave before a participant-joined fact exists."

        if candidate.category == BusinessFactCategory.BF_008_DISCUSSION_CLOSED:
            discussion_id = self._reference_id(candidate, "Discussion")
            if discussion_id and not self._has_category_with_reference(
                history,
                BusinessFactCategory.BF_007_DISCUSSION_STARTED,
                "Discussion",
                discussion_id,
                meeting_id=candidate.meeting_id,
            ):
                return "Discussion cannot be closed before a discussion-started fact exists."

        if candidate.category == BusinessFactCategory.BF_013_VOTE_CLOSED:
            vote_id = self._reference_id(candidate, "Vote")
            if vote_id and not self._has_category_with_reference(
                history,
                BusinessFactCategory.BF_012_VOTE_STARTED,
                "Vote",
                vote_id,
                meeting_id=candidate.meeting_id,
            ):
                return "Vote cannot be closed before a vote-started fact exists."

        if candidate.category in {
            BusinessFactCategory.BF_014_RESOLUTION_APPROVED,
            BusinessFactCategory.BF_015_RESOLUTION_REJECTED,
        }:
            resolution_id = self._reference_id(candidate, "Resolution")
            opposite = {
                BusinessFactCategory.BF_014_RESOLUTION_APPROVED: (
                    BusinessFactCategory.BF_015_RESOLUTION_REJECTED
                ),
                BusinessFactCategory.BF_015_RESOLUTION_REJECTED: (
                    BusinessFactCategory.BF_014_RESOLUTION_APPROVED
                ),
            }[candidate.category]
            if resolution_id and self._has_category_with_reference(
                history,
                opposite,
                "Resolution",
                resolution_id,
                meeting_id=candidate.meeting_id,
            ):
                return "Resolution cannot be both approved and rejected without corrective flow."

        if candidate.category == BusinessFactCategory.BF_010_MOTION_AMENDED:
            motion_id = self._reference_id(candidate, "Motion")
            if motion_id and self._has_category_with_reference(
                history,
                BusinessFactCategory.BF_011_MOTION_WITHDRAWN,
                "Motion",
                motion_id,
                meeting_id=candidate.meeting_id,
            ):
                return "Motion cannot be amended after a motion-withdrawn fact exists."

        return None

    @staticmethod
    def _reference_id(fact: BusinessFact, concept_type: str) -> str | None:
        for reference in fact.references:
            if reference.concept_type == concept_type:
                return reference.concept_id
        return None

    @staticmethod
    def _has_category(
        history: BusinessFactLog,
        category: BusinessFactCategory,
        *,
        meeting_id: str,
    ) -> bool:
        return any(
            fact.category == category and fact.meeting_id == meeting_id for fact in history.facts
        )

    @staticmethod
    def _has_category_with_reference(
        history: BusinessFactLog,
        category: BusinessFactCategory,
        concept_type: str,
        concept_id: str,
        *,
        meeting_id: str,
    ) -> bool:
        for fact in history.facts:
            if fact.category != category or fact.meeting_id != meeting_id:
                continue
            for reference in fact.references:
                if reference.concept_type == concept_type and reference.concept_id == concept_id:
                    return True
        return False
