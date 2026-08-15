"""Aggregate roots and core entities for the business domain."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from domain.value_objects import ParticipantRole, PersonName, VoteCount


def _require_id(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _lock_identity(instance: object, field_name: str, value: str) -> None:
    if hasattr(instance, field_name):
        raise AttributeError(f"{field_name} is immutable once set")
    object.__setattr__(instance, field_name, value)


class MeetingStatus(str, Enum):
    CREATED = "created"
    CLOSED = "closed"


@dataclass(slots=True)
class Organization:
    name: str
    id: str
    meetings: list[Meeting] = field(default_factory=list)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Organization.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Organization.name must be a non-empty string")
        self.name = self.name.strip()

    def add_meeting(self, meeting: Meeting) -> None:
        if meeting.organization_id != self.id:
            raise ValueError("Meeting.organization_id must match Organization.id")
        self.meetings.append(meeting)


@dataclass(slots=True)
class Meeting:
    id: str
    organization_id: str
    created_at: datetime
    status: MeetingStatus = MeetingStatus.CREATED
    closed_at: datetime | None = None
    participants: list[Participant] = field(default_factory=list)
    discussions: list[Discussion] = field(default_factory=list)
    agenda: Agenda | None = None
    attachments: list[Attachment] = field(default_factory=list)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Meeting.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.organization_id = _require_id(self.organization_id, "Meeting.organization_id")

    @property
    def is_closed(self) -> bool:
        return self.status == MeetingStatus.CLOSED

    def close(self, closed_at: datetime) -> None:
        if self.is_closed:
            raise ValueError("Meeting is already closed")
        self.status = MeetingStatus.CLOSED
        self.closed_at = closed_at

    def _ensure_open(self) -> None:
        if self.is_closed:
            raise ValueError("Meeting is closed and can no longer be modified")

    def add_participant(self, participant: Participant) -> None:
        self._ensure_open()
        if participant.meeting_id != self.id:
            raise ValueError("Participant.meeting_id must match Meeting.id")
        self.participants.append(participant)

    def add_discussion(self, discussion: Discussion) -> None:
        self._ensure_open()
        if discussion.meeting_id != self.id:
            raise ValueError("Discussion.meeting_id must match Meeting.id")
        self.discussions.append(discussion)

    def set_agenda(self, agenda: Agenda) -> None:
        self._ensure_open()
        if agenda.meeting_id != self.id:
            raise ValueError("Agenda.meeting_id must match Meeting.id")
        if self.agenda is not None:
            raise ValueError("Meeting can contain only one Agenda")
        self.agenda = agenda

    def add_attachment(self, attachment: Attachment) -> None:
        self._ensure_open()
        if attachment.meeting_id != self.id:
            raise ValueError("Attachment.meeting_id must match Meeting.id")
        self.attachments.append(attachment)


@dataclass(slots=True)
class Person:
    id: str
    organization_id: str
    name: PersonName

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Person.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.organization_id = _require_id(self.organization_id, "Person.organization_id")


@dataclass(slots=True)
class Participant:
    id: str
    meeting_id: str
    person_id: str
    role: ParticipantRole

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Participant.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.meeting_id = _require_id(self.meeting_id, "Participant.meeting_id")
        self.person_id = _require_id(self.person_id, "Participant.person_id")


@dataclass(slots=True)
class Agenda:
    id: str
    meeting_id: str
    items: list[AgendaItem]

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Agenda.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.meeting_id = _require_id(self.meeting_id, "Agenda.meeting_id")
        if not self.items:
            raise ValueError("Agenda.items must contain one or more AgendaItem")
        for item in self.items:
            if item.agenda_id != self.id:
                raise ValueError("AgendaItem.agenda_id must match Agenda.id")


@dataclass(slots=True)
class AgendaItem:
    id: str
    agenda_id: str

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "AgendaItem.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.agenda_id = _require_id(self.agenda_id, "AgendaItem.agenda_id")


@dataclass(slots=True)
class Discussion:
    id: str
    meeting_id: str
    agenda_item_id: str
    interventions: list[Intervention] = field(default_factory=list)
    motions: list[Motion] = field(default_factory=list)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Discussion.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.meeting_id = _require_id(self.meeting_id, "Discussion.meeting_id")
        self.agenda_item_id = _require_id(self.agenda_item_id, "Discussion.agenda_item_id")

    def add_intervention(self, intervention: Intervention) -> None:
        if intervention.discussion_id != self.id:
            raise ValueError("Intervention.discussion_id must match Discussion.id")
        self.interventions.append(intervention)

    def add_motion(self, motion: Motion) -> None:
        if motion.discussion_id != self.id:
            raise ValueError("Motion.discussion_id must match Discussion.id")
        self.motions.append(motion)


@dataclass(slots=True)
class Intervention:
    id: str
    discussion_id: str
    participant_id: str

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Intervention.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.discussion_id = _require_id(self.discussion_id, "Intervention.discussion_id")
        self.participant_id = _require_id(self.participant_id, "Intervention.participant_id")


@dataclass(slots=True)
class Motion:
    id: str
    discussion_id: str
    vote: Vote | None = None
    resolutions: list[Resolution] = field(default_factory=list)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Motion.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.discussion_id = _require_id(self.discussion_id, "Motion.discussion_id")

    def set_vote(self, vote: Vote) -> None:
        if vote.motion_id != self.id:
            raise ValueError("Vote.motion_id must match Motion.id")
        if self.vote is not None:
            raise ValueError("Motion can have at most one Vote")
        self.vote = vote

    def add_resolution(self, resolution: Resolution) -> None:
        if resolution.motion_id != self.id:
            raise ValueError("Resolution.motion_id must match Motion.id")
        self.resolutions.append(resolution)


@dataclass(slots=True)
class Vote:
    id: str
    motion_id: str
    count: VoteCount

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Vote.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.motion_id = _require_id(self.motion_id, "Vote.motion_id")


@dataclass(slots=True)
class Resolution:
    id: str
    meeting_id: str
    motion_id: str
    actions: list[Action] = field(default_factory=list)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Resolution.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.meeting_id = _require_id(self.meeting_id, "Resolution.meeting_id")
        self.motion_id = _require_id(self.motion_id, "Resolution.motion_id")

    def add_action(self, action: Action) -> None:
        if action.resolution_id != self.id:
            raise ValueError("Action.resolution_id must match Resolution.id")
        if action.meeting_id != self.meeting_id:
            raise ValueError("Action.meeting_id must match Resolution.meeting_id")
        self.actions.append(action)


@dataclass(slots=True)
class Action:
    id: str
    meeting_id: str
    resolution_id: str

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Action.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.meeting_id = _require_id(self.meeting_id, "Action.meeting_id")
        self.resolution_id = _require_id(self.resolution_id, "Action.resolution_id")


@dataclass(slots=True)
class Attachment:
    id: str
    meeting_id: str
    name: str

    def __setattr__(self, name: str, value: object) -> None:
        if name == "id":
            _lock_identity(self, "id", _require_id(value, "Attachment.id"))  # type: ignore[arg-type]
            return
        object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.meeting_id = _require_id(self.meeting_id, "Attachment.meeting_id")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Attachment.name must be a non-empty string")
        self.name = self.name.strip()
