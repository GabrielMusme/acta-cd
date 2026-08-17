from datetime import datetime

import pytest

from domain.entities import (
    Action,
    Agenda,
    AgendaItem,
    Discussion,
    Intervention,
    Meeting,
    MeetingStatus,
    Motion,
    Organization,
    Participant,
    Person,
    Resolution,
    Vote,
)
from domain.value_objects import ParticipantRole, PersonName, VoteCount

pytestmark = [pytest.mark.phase1_gate]


def _meeting() -> Meeting:
    return Meeting(
        id="meeting-1",
        organization_id="org-1",
        created_at=datetime(2026, 8, 15, 10, 0, 0),
    )


def test_identity_is_stable_for_entities_and_aggregates() -> None:
    organization = Organization(id="org-1", name="Board")

    with pytest.raises(AttributeError):
        organization.id = "org-2"


def test_organization_contains_only_owned_meetings() -> None:
    organization = Organization(id="org-1", name="Board")
    owned = Meeting(id="meeting-1", organization_id="org-1", created_at=datetime.now())
    foreign = Meeting(id="meeting-2", organization_id="org-2", created_at=datetime.now())

    organization.add_meeting(owned)
    assert organization.meetings == [owned]

    with pytest.raises(ValueError):
        organization.add_meeting(foreign)


def test_participant_must_belong_to_exactly_one_meeting() -> None:
    meeting = _meeting()
    person = Person(id="person-1", organization_id="org-1", name=PersonName("Alice"))
    participant = Participant(
        id="participant-1",
        meeting_id=meeting.id,
        person_id=person.id,
        role=ParticipantRole("Chair"),
    )

    meeting.add_participant(participant)
    assert meeting.participants == [participant]

    with pytest.raises(ValueError):
        meeting.add_participant(
            Participant(
                id="participant-2",
                meeting_id="other-meeting",
                person_id=person.id,
                role=ParticipantRole("Member"),
            )
        )


def test_agenda_requires_at_least_one_item_and_matching_parent() -> None:
    with pytest.raises(ValueError):
        Agenda(id="agenda-1", meeting_id="meeting-1", items=[])

    with pytest.raises(ValueError):
        Agenda(
            id="agenda-1",
            meeting_id="meeting-1",
            items=[AgendaItem(id="item-1", agenda_id="agenda-2")],
        )


def test_meeting_contains_at_most_one_agenda() -> None:
    meeting = _meeting()
    first = Agenda(
        id="agenda-1",
        meeting_id=meeting.id,
        items=[AgendaItem(id="item-1", agenda_id="agenda-1")],
    )
    second = Agenda(
        id="agenda-2",
        meeting_id=meeting.id,
        items=[AgendaItem(id="item-2", agenda_id="agenda-2")],
    )

    meeting.set_agenda(first)
    assert meeting.agenda == first

    with pytest.raises(ValueError):
        meeting.set_agenda(second)


def test_discussion_intervention_and_motion_parent_constraints() -> None:
    discussion = Discussion(id="discussion-1", meeting_id="meeting-1", agenda_item_id="item-1")
    participant = Participant(
        id="participant-1",
        meeting_id="meeting-1",
        person_id="person-1",
        role=ParticipantRole("Member"),
    )
    intervention = Intervention(
        id="intervention-1",
        discussion_id=discussion.id,
        participant_id=participant.id,
    )
    discussion.add_intervention(intervention)
    assert discussion.interventions == [intervention]

    with pytest.raises(ValueError):
        discussion.add_intervention(
            Intervention(
                id="intervention-2",
                discussion_id="other-discussion",
                participant_id=participant.id,
            )
        )

    motion = Motion(id="motion-1", discussion_id=discussion.id)
    discussion.add_motion(motion)
    assert discussion.motions == [motion]


def test_vote_and_resolution_constraints() -> None:
    motion = Motion(id="motion-1", discussion_id="discussion-1")
    vote = Vote(id="vote-1", motion_id=motion.id, count=VoteCount(yes=2, no=1))
    motion.set_vote(vote)
    assert motion.vote == vote

    with pytest.raises(ValueError):
        motion.set_vote(Vote(id="vote-2", motion_id="other-motion", count=VoteCount(yes=1, no=0)))

    resolution = Resolution(id="res-1", meeting_id="meeting-1", motion_id=motion.id)
    action = Action(id="action-1", meeting_id="meeting-1", resolution_id=resolution.id)
    resolution.add_action(action)
    assert resolution.actions == [action]

    with pytest.raises(ValueError):
        resolution.add_action(
            Action(id="action-2", meeting_id="meeting-2", resolution_id=resolution.id)
        )


def test_meeting_lifecycle_blocks_mutations_after_closure() -> None:
    meeting = _meeting()
    person = Person(id="person-1", organization_id="org-1", name=PersonName("Alice"))
    participant = Participant(
        id="participant-1",
        meeting_id=meeting.id,
        person_id=person.id,
        role=ParticipantRole("Secretary"),
    )

    meeting.add_participant(participant)
    meeting.close(datetime(2026, 8, 15, 12, 0, 0))

    assert meeting.status == MeetingStatus.CLOSED
    assert meeting.closed_at is not None
    assert meeting.participants == [participant]

    with pytest.raises(ValueError):
        meeting.add_participant(
            Participant(
                id="participant-2",
                meeting_id=meeting.id,
                person_id=person.id,
                role=ParticipantRole("Member"),
            )
        )
