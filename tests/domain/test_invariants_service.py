from dataclasses import dataclass
from datetime import datetime

import pytest

from domain.entities import (
    Action,
    Discussion,
    Meeting,
    Motion,
    Participant,
    Person,
    Resolution,
    Vote,
)
from domain.services import (
    BusinessFactRecord,
    DMI001Error,
    DMI002Error,
    DMI003Error,
    DMI004Error,
    DMI005Error,
    DMI006Error,
    DMI007Error,
    DMI008Error,
    DMI009Error,
    DMI010Error,
    DMI011Error,
    DMI012Error,
    DMI013Error,
    DMI014Error,
    DMI015Error,
    DomainInvariantContext,
    DomainInvariantValidator,
    IdentitySnapshot,
)
from domain.value_objects import ParticipantRole, PersonName, VoteCount


@dataclass
class _FakeValueObjectWithId:
    id: str


def _build_valid_context() -> DomainInvariantContext:
    meeting = Meeting(
        id="meeting-1",
        organization_id="org-1",
        created_at=datetime(2026, 8, 15, 10, 0, 0),
    )
    person = Person(id="person-1", organization_id="org-1", name=PersonName("Alice"))
    participant = Participant(
        id="participant-1",
        meeting_id=meeting.id,
        person_id=person.id,
        role=ParticipantRole("Chair"),
    )
    discussion = Discussion(
        id="discussion-1", meeting_id=meeting.id, agenda_item_id="agenda-item-1"
    )
    motion = Motion(id="motion-1", discussion_id=discussion.id)
    vote = Vote(id="vote-1", motion_id=motion.id, count=VoteCount(yes=2, no=1, abstain=0))
    resolution = Resolution(id="resolution-1", meeting_id=meeting.id, motion_id=motion.id)
    action = Action(id="action-1", meeting_id=meeting.id, resolution_id=resolution.id)

    return DomainInvariantContext(
        meetings=[meeting],
        persons=[person],
        participants=[participant],
        discussions=[discussion],
        motions=[motion],
        votes=[vote],
        resolutions=[resolution],
        actions=[action],
        business_facts=[BusinessFactRecord(meeting_id=meeting.id, immutable=True, rewrite_count=0)],
        value_objects=[PersonName("Alice"), ParticipantRole("Chair")],
        identity_snapshots=[
            IdentitySnapshot(entity_type="Meeting", initial_id=meeting.id, current_id=meeting.id)
        ],
        history_rewritten=False,
        processing_concepts=[],
        knowledge_redefinitions=[],
        human_artifact_inputs=[],
    )


def test_all_invariants_pass_for_valid_context() -> None:
    context = _build_valid_context()
    DomainInvariantValidator().validate_all(context)


def test_dmi_001_rejects_value_object_with_identity() -> None:
    context = _build_valid_context()
    context.value_objects = [_FakeValueObjectWithId(id="vo-1")]

    with pytest.raises(DMI001Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_002_rejects_identity_drift() -> None:
    context = _build_valid_context()
    context.identity_snapshots = [
        IdentitySnapshot(entity_type="Meeting", initial_id="meeting-1", current_id="meeting-2")
    ]

    with pytest.raises(DMI002Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_003_rejects_mutable_business_fact() -> None:
    context = _build_valid_context()
    context.business_facts = [
        BusinessFactRecord(meeting_id="meeting-1", immutable=False, rewrite_count=0)
    ]

    with pytest.raises(DMI003Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_004_rejects_history_rewrite_marker() -> None:
    context = _build_valid_context()
    context.history_rewritten = True

    with pytest.raises(DMI004Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_005_rejects_invalid_participant_after_meeting_closure() -> None:
    context = _build_valid_context()
    context.meetings[0].close(datetime(2026, 8, 15, 12, 0, 0))
    context.participants[0].person_id = ""

    with pytest.raises(DMI005Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_006_rejects_participant_without_person_reference() -> None:
    context = _build_valid_context()
    context.participants[0].person_id = "unknown-person"

    with pytest.raises(DMI006Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_007_rejects_participant_without_meeting() -> None:
    context = _build_valid_context()
    context.participants[0].meeting_id = "unknown-meeting"

    with pytest.raises(DMI007Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_008_rejects_discussion_without_meeting() -> None:
    context = _build_valid_context()
    context.discussions[0].meeting_id = "unknown-meeting"

    with pytest.raises(DMI008Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_009_rejects_motion_without_discussion() -> None:
    context = _build_valid_context()
    context.motions[0].discussion_id = "unknown-discussion"

    with pytest.raises(DMI009Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_010_rejects_vote_without_motion() -> None:
    context = _build_valid_context()
    context.votes[0].motion_id = "unknown-motion"

    with pytest.raises(DMI010Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_011_rejects_action_without_resolution() -> None:
    context = _build_valid_context()
    context.actions[0].resolution_id = "unknown-resolution"

    with pytest.raises(DMI011Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_012_rejects_business_fact_without_meeting() -> None:
    context = _build_valid_context()
    context.business_facts = [
        BusinessFactRecord(meeting_id="unknown-meeting", immutable=True, rewrite_count=0)
    ]

    with pytest.raises(DMI012Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_013_rejects_processing_concepts_in_business_domain() -> None:
    context = _build_valid_context()
    context.processing_concepts = ["queue", "worker"]

    with pytest.raises(DMI013Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_014_rejects_knowledge_redefinition() -> None:
    context = _build_valid_context()
    context.knowledge_redefinitions = ["redefined meeting concept"]

    with pytest.raises(DMI014Error):
        DomainInvariantValidator().validate_all(context)


def test_dmi_015_rejects_human_artifact_as_business_reality() -> None:
    context = _build_valid_context()
    context.human_artifact_inputs = ["minutes.md"]

    with pytest.raises(DMI015Error):
        DomainInvariantValidator().validate_all(context)


def test_validate_and_collect_returns_deterministic_errors() -> None:
    context = _build_valid_context()
    context.processing_concepts = ["worker"]
    context.knowledge_redefinitions = ["redefinition"]

    errors = DomainInvariantValidator().validate_and_collect(context)
    error_ids = [error.invariant_id for error in errors]

    assert error_ids == ["DMI-013", "DMI-014"]
