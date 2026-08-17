from datetime import datetime

import pytest

from business_facts.models import BusinessFact, BusinessFactCategory, ConceptReference
from domain.entities import (
    Action,
    Agenda,
    AgendaItem,
    Attachment,
    Discussion,
    Meeting,
    Motion,
    Participant,
    Person,
    Resolution,
    Vote,
)
from domain.services import DomainFactLinkingService
from domain.value_objects import ParticipantRole, PersonName, VoteCount

pytestmark = [pytest.mark.phase1_gate]


def _domain_fixture() -> tuple[Meeting, Person, Resolution, Action, Vote]:
    meeting = Meeting(
        id="meeting-1",
        organization_id="org-1",
        created_at=datetime(2026, 8, 16, 9, 0, 0),
    )

    person = Person(id="person-1", organization_id="org-1", name=PersonName("Alice"))
    participant = Participant(
        id="participant-1",
        meeting_id=meeting.id,
        person_id=person.id,
        role=ParticipantRole("Chair"),
    )
    meeting.add_participant(participant)

    agenda = Agenda(
        id="agenda-1",
        meeting_id=meeting.id,
        items=[AgendaItem(id="agenda-item-1", agenda_id="agenda-1")],
    )
    meeting.set_agenda(agenda)

    discussion = Discussion(
        id="discussion-1",
        meeting_id=meeting.id,
        agenda_item_id="agenda-item-1",
    )
    meeting.add_discussion(discussion)

    motion = Motion(id="motion-1", discussion_id=discussion.id)
    discussion.add_motion(motion)

    vote = Vote(id="vote-1", motion_id=motion.id, count=VoteCount(yes=3, no=1))
    motion.set_vote(vote)

    resolution = Resolution(id="resolution-1", meeting_id=meeting.id, motion_id=motion.id)
    motion.add_resolution(resolution)

    action = Action(id="action-1", meeting_id=meeting.id, resolution_id=resolution.id)
    resolution.add_action(action)

    meeting.add_attachment(Attachment(id="attachment-1", meeting_id=meeting.id, name="agenda.pdf"))

    return meeting, person, resolution, action, vote


def _fact(
    *,
    fact_id: str,
    category: BusinessFactCategory,
    references: tuple[ConceptReference, ...],
    meeting_id: str = "meeting-1",
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


def test_linking_service_links_accepted_facts_with_domain_fixture() -> None:
    meeting, person, resolution, action, vote = _domain_fixture()
    service = DomainFactLinkingService()

    facts = (
        _fact(
            fact_id="fact-1",
            category=BusinessFactCategory.BF_001_MEETING_CREATED,
            references=(
                ConceptReference("Organization", "org-1"),
                ConceptReference("Meeting", "meeting-1"),
            ),
        ),
        _fact(
            fact_id="fact-2",
            category=BusinessFactCategory.BF_004_PARTICIPANT_JOINED,
            references=(
                ConceptReference("Participant", "participant-1"),
                ConceptReference("Meeting", "meeting-1"),
                ConceptReference("Person", "person-1"),
            ),
        ),
        _fact(
            fact_id="fact-3",
            category=BusinessFactCategory.BF_014_RESOLUTION_APPROVED,
            references=(
                ConceptReference("Resolution", resolution.id),
                ConceptReference("Motion", "motion-1"),
            ),
        ),
        _fact(
            fact_id="fact-4",
            category=BusinessFactCategory.BF_016_ACTION_ASSIGNED,
            references=(
                ConceptReference("Action", action.id),
                ConceptReference("Resolution", resolution.id),
            ),
        ),
        _fact(
            fact_id="fact-5",
            category=BusinessFactCategory.BF_013_VOTE_CLOSED,
            references=(
                ConceptReference("Vote", vote.id),
                ConceptReference("Motion", "motion-1"),
            ),
        ),
    )

    result = service.link_accepted_facts(meeting=meeting, accepted_facts=facts, persons=[person])

    assert len(result.linked) == 5
    assert not result.rejected
    assert sum(len(item.links) for item in result.linked) == 11


def test_linking_rejects_fact_outside_meeting_context() -> None:
    meeting, person, _, _, _ = _domain_fixture()
    service = DomainFactLinkingService()

    unknown_participant_fact = _fact(
        fact_id="fact-bad-1",
        category=BusinessFactCategory.BF_004_PARTICIPANT_JOINED,
        references=(
            ConceptReference("Participant", "participant-404"),
            ConceptReference("Meeting", "meeting-1"),
            ConceptReference("Person", person.id),
        ),
    )

    result = service.link_accepted_facts(meeting=meeting, accepted_facts=[unknown_participant_fact])

    assert not result.linked
    assert len(result.rejected) == 1
    error = result.rejected[0][1]
    assert error.code == "DFL-003"
    assert error.reason == "concept_outside_meeting_context"


def test_linking_rejects_fact_with_mismatched_meeting() -> None:
    meeting, _, _, _, _ = _domain_fixture()
    service = DomainFactLinkingService()

    wrong_meeting_fact = _fact(
        fact_id="fact-bad-2",
        category=BusinessFactCategory.BF_002_MEETING_STARTED,
        meeting_id="meeting-2",
        references=(ConceptReference("Meeting", "meeting-1"),),
    )

    result = service.link_accepted_facts(meeting=meeting, accepted_facts=[wrong_meeting_fact])

    assert not result.linked
    assert len(result.rejected) == 1
    error = result.rejected[0][1]
    assert error.code == "DFL-001"
    assert error.reason == "meeting_mismatch"


def test_linking_rejects_unsupported_concept_type() -> None:
    meeting, _, _, _, _ = _domain_fixture()
    service = DomainFactLinkingService()

    unsupported_ref_fact = _fact(
        fact_id="fact-bad-3",
        category=BusinessFactCategory.BF_018_DOCUMENT_REFERENCED,
        references=(
            ConceptReference("Document", "doc-1"),
            ConceptReference("Meeting", "meeting-1"),
        ),
    )

    result = service.link_accepted_facts(meeting=meeting, accepted_facts=[unsupported_ref_fact])

    assert not result.linked
    assert len(result.rejected) == 1
    error = result.rejected[0][1]
    assert error.code == "DFL-002"
    assert error.reason == "unsupported_concept_type"


def test_linking_does_not_mutate_business_fact_content() -> None:
    meeting, person, _, _, _ = _domain_fixture()
    service = DomainFactLinkingService()

    fact = _fact(
        fact_id="fact-immutability",
        category=BusinessFactCategory.BF_004_PARTICIPANT_JOINED,
        references=(
            ConceptReference("Participant", "participant-1"),
            ConceptReference("Meeting", "meeting-1"),
            ConceptReference("Person", "person-1"),
        ),
        payload={"source": "integration-test"},
    )

    before_refs = fact.references
    before_payload = dict(fact.payload)

    result = service.link_accepted_facts(meeting=meeting, accepted_facts=[fact], persons=[person])

    assert len(result.linked) == 1
    assert not result.rejected
    assert fact.references == before_refs
    assert dict(fact.payload) == before_payload
