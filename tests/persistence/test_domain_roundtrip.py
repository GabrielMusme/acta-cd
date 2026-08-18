from __future__ import annotations

import os
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from domain.entities.core import Action, Agenda, AgendaItem, Attachment, Discussion, Intervention, Meeting, MeetingStatus, Motion, Organization, Participant, Person, Resolution, Vote
from domain.value_objects.core import ParticipantRole, PersonName, VoteCount
from infrastructure.persistence.models import Base, ActionModel, AgendaItemModel, AgendaModel, AttachmentModel, DiscussionModel, InterventionModel, MeetingModel, MotionModel, OrganizationModel, ParticipantModel, PersonModel, ResolutionModel, VoteModel


@pytest.mark.skipif(not os.getenv("ACTA_DATABASE_URL"), reason="requires ACTA_DATABASE_URL")
def test_domain_roundtrip_persists_core_entities() -> None:
    engine = create_engine(os.environ["ACTA_DATABASE_URL"], future=True)
    Base.metadata.create_all(engine)

    now = datetime.now(timezone.utc)
    org = Organization(id="org-01", name="Example Org")
    meeting = Meeting(id="meeting-01", organization_id="org-01", created_at=now)
    person = Person(id="person-01", organization_id="org-01", name=PersonName("Jane Doe"))
    participant = Participant(id="participant-01", meeting_id="meeting-01", person_id="person-01", role=ParticipantRole("host"))
    agenda = Agenda(id="agenda-01", meeting_id="meeting-01", items=[AgendaItem(id="agenda-item-01", agenda_id="agenda-01")])
    discussion = Discussion(id="discussion-01", meeting_id="meeting-01", agenda_item_id="agenda-item-01")
    intervention = Intervention(id="intervention-01", discussion_id="discussion-01", participant_id="participant-01")
    motion = Motion(id="motion-01", discussion_id="discussion-01")
    vote = Vote(id="vote-01", motion_id="motion-01", count=VoteCount(yes=2, no=1, abstain=1))
    resolution = Resolution(id="resolution-01", meeting_id="meeting-01", motion_id="motion-01")
    action = Action(id="action-01", meeting_id="meeting-01", resolution_id="resolution-01")
    attachment = Attachment(id="attachment-01", meeting_id="meeting-01", name="minutes.pdf")

    with Session(engine) as session:
        session.add(OrganizationModel(id=org.id, name=org.name, created_at=now, updated_at=now))
        session.add(MeetingModel(id=meeting.id, organization_id=meeting.organization_id, status=meeting.status.value, created_at=now, closed_at=meeting.closed_at, updated_at=now))
        session.add(PersonModel(id=person.id, organization_id=person.organization_id, display_name=person.name.value, created_at=now, updated_at=now))
        session.add(ParticipantModel(id=participant.id, meeting_id=participant.meeting_id, person_id=participant.person_id, role=participant.role.value, created_at=now, updated_at=now))
        session.add(AgendaModel(id=agenda.id, meeting_id=agenda.meeting_id, created_at=now, updated_at=now))
        session.add(AgendaItemModel(id=agenda.items[0].id, agenda_id=agenda.id, created_at=now, updated_at=now))
        session.add(DiscussionModel(id=discussion.id, meeting_id=discussion.meeting_id, agenda_item_id=discussion.agenda_item_id, created_at=now, updated_at=now))
        session.add(InterventionModel(id=intervention.id, discussion_id=intervention.discussion_id, participant_id=intervention.participant_id, created_at=now, updated_at=now))
        session.add(MotionModel(id=motion.id, discussion_id=motion.discussion_id, created_at=now, updated_at=now))
        session.add(VoteModel(id=vote.id, motion_id=vote.motion_id, yes_count=vote.count.yes, no_count=vote.count.no, abstain_count=vote.count.abstain, created_at=now, updated_at=now))
        session.add(ResolutionModel(id=resolution.id, meeting_id=resolution.meeting_id, motion_id=resolution.motion_id, created_at=now, updated_at=now))
        session.add(ActionModel(id=action.id, meeting_id=action.meeting_id, resolution_id=action.resolution_id, created_at=now, updated_at=now))
        session.add(AttachmentModel(id=attachment.id, meeting_id=attachment.meeting_id, name=attachment.name, created_at=now, updated_at=now))
        session.commit()

    with Session(engine) as session:
        org_row = session.get(OrganizationModel, "org-01")
        meeting_row = session.get(MeetingModel, "meeting-01")
        person_row = session.get(PersonModel, "person-01")
        participant_row = session.get(ParticipantModel, "participant-01")
        agenda_row = session.get(AgendaModel, "agenda-01")
        discussion_row = session.get(DiscussionModel, "discussion-01")

        assert org_row is not None and org_row.name == org.name
        assert meeting_row is not None and meeting_row.organization_id == org.id
        assert person_row is not None and person_row.display_name == person.name.value
        assert participant_row is not None and participant_row.role == participant.role.value
        assert agenda_row is not None and agenda_row.meeting_id == meeting.id
        assert discussion_row is not None and discussion_row.meeting_id == meeting.id

    Base.metadata.drop_all(engine)
