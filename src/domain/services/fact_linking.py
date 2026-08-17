"""Domain-Facts linking service."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from business_facts.models import BusinessFact
from domain.entities import Action, Meeting, Motion, Person, Resolution, Vote


@dataclass(frozen=True, slots=True)
class FactLinkingError:
    code: str
    reason: str
    fact_id: str
    details: str


@dataclass(frozen=True, slots=True)
class FactConceptLink:
    fact_id: str
    concept_type: str
    concept_id: str


@dataclass(frozen=True, slots=True)
class LinkedFact:
    fact: BusinessFact
    links: tuple[FactConceptLink, ...]


@dataclass(frozen=True, slots=True)
class FactLinkingBatchResult:
    linked: tuple[LinkedFact, ...]
    rejected: tuple[tuple[BusinessFact, FactLinkingError], ...]


class DomainFactLinkingService:
    """Attach accepted facts to related domain concepts without mutating facts."""

    def link_accepted_facts(
        self,
        *,
        meeting: Meeting,
        accepted_facts: Iterable[BusinessFact],
        persons: Iterable[Person] = (),
        motions: Iterable[Motion] = (),
        votes: Iterable[Vote] = (),
        resolutions: Iterable[Resolution] = (),
        actions: Iterable[Action] = (),
    ) -> FactLinkingBatchResult:
        registry = self._build_registry(
            meeting=meeting,
            persons=persons,
            motions=motions,
            votes=votes,
            resolutions=resolutions,
            actions=actions,
        )

        linked: list[LinkedFact] = []
        rejected: list[tuple[BusinessFact, FactLinkingError]] = []

        for fact in accepted_facts:
            error = self._validate_fact_context(fact=fact, meeting=meeting, registry=registry)
            if error is not None:
                rejected.append((fact, error))
                continue

            links = tuple(
                FactConceptLink(
                    fact_id=fact.fact_id,
                    concept_type=reference.concept_type,
                    concept_id=reference.concept_id,
                )
                for reference in fact.references
            )
            linked.append(LinkedFact(fact=fact, links=links))

        return FactLinkingBatchResult(linked=tuple(linked), rejected=tuple(rejected))

    def _validate_fact_context(
        self,
        *,
        fact: BusinessFact,
        meeting: Meeting,
        registry: Mapping[str, frozenset[str]],
    ) -> FactLinkingError | None:
        if fact.meeting_id != meeting.id:
            return FactLinkingError(
                code="DFL-001",
                reason="meeting_mismatch",
                fact_id=fact.fact_id,
                details="Fact meeting_id does not match target meeting context.",
            )

        for reference in fact.references:
            known_ids = registry.get(reference.concept_type)
            if known_ids is None:
                return FactLinkingError(
                    code="DFL-002",
                    reason="unsupported_concept_type",
                    fact_id=fact.fact_id,
                    details=f"Unsupported concept type for linking: {reference.concept_type}",
                )

            if reference.concept_id not in known_ids:
                return FactLinkingError(
                    code="DFL-003",
                    reason="concept_outside_meeting_context",
                    fact_id=fact.fact_id,
                    details=(
                        f"Concept {reference.concept_type}:{reference.concept_id} "
                        "is not present in the meeting context registry."
                    ),
                )

        return None

    def _build_registry(
        self,
        *,
        meeting: Meeting,
        persons: Iterable[Person],
        motions: Iterable[Motion],
        votes: Iterable[Vote],
        resolutions: Iterable[Resolution],
        actions: Iterable[Action],
    ) -> Mapping[str, frozenset[str]]:
        person_ids = {participant.person_id for participant in meeting.participants}
        person_ids.update(person.id for person in persons)

        motion_ids = {motion.id for motion in motions}
        vote_ids = {vote.id for vote in votes}
        resolution_ids = {resolution.id for resolution in resolutions}
        action_ids = {action.id for action in actions}

        for discussion in meeting.discussions:
            for motion in discussion.motions:
                motion_ids.add(motion.id)
                if motion.vote is not None:
                    vote_ids.add(motion.vote.id)
                for resolution in motion.resolutions:
                    resolution_ids.add(resolution.id)
                    for action in resolution.actions:
                        action_ids.add(action.id)

        agenda_ids = {meeting.agenda.id} if meeting.agenda is not None else set()
        agenda_item_ids = {item.id for item in meeting.agenda.items} if meeting.agenda else set()

        registry: dict[str, frozenset[str]] = {
            "Organization": frozenset({meeting.organization_id}),
            "Meeting": frozenset({meeting.id}),
            "Participant": frozenset(participant.id for participant in meeting.participants),
            "Person": frozenset(person_ids),
            "Agenda": frozenset(agenda_ids),
            "AgendaItem": frozenset(agenda_item_ids),
            "Discussion": frozenset(discussion.id for discussion in meeting.discussions),
            "Motion": frozenset(motion_ids),
            "Vote": frozenset(vote_ids),
            "Resolution": frozenset(resolution_ids),
            "Action": frozenset(action_ids),
            "Attachment": frozenset(attachment.id for attachment in meeting.attachments),
        }
        return MappingProxyType(registry)
