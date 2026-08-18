from __future__ import annotations

import random
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, event, func


def _uuid7() -> str:
    """Return a valid UUIDv7 identifier in canonical string form."""
    unix_ts_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    rand_a = random.getrandbits(12)
    rand_b = random.getrandbits(62)
    uuid_int = ((unix_ts_ms & 0xFFFFFFFFFFFF) << 64) | ((7 << 12) << 52) | ((rand_a & 0xFFF) << 52) | (rand_b & ((1 << 62) - 1))
    return str(UUID(int=uuid_int))


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    meetings: Mapped[list[MeetingModel]] = relationship(back_populates="organization")
    people: Mapped[list[PersonModel]] = relationship(back_populates="organization")


class MeetingModel(Base):
    __tablename__ = "meetings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="created")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped[OrganizationModel] = relationship(back_populates="meetings")
    participants: Mapped[list[ParticipantModel]] = relationship(back_populates="meeting")
    agenda: Mapped[AgendaModel | None] = relationship(back_populates="meeting", uselist=False)
    discussions: Mapped[list[DiscussionModel]] = relationship(back_populates="meeting")
    attachments: Mapped[list[AttachmentModel]] = relationship(back_populates="meeting")
    business_facts: Mapped[list[BusinessFactModel]] = relationship(back_populates="meeting")


class PersonModel(Base):
    __tablename__ = "people"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped[OrganizationModel] = relationship(back_populates="people")
    participants: Mapped[list[ParticipantModel]] = relationship(back_populates="person")


class ParticipantModel(Base):
    __tablename__ = "participants"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    meeting_id: Mapped[str] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    person_id: Mapped[str] = mapped_column(ForeignKey("people.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    meeting: Mapped[MeetingModel] = relationship(back_populates="participants")
    person: Mapped[PersonModel] = relationship(back_populates="participants")
    interventions: Mapped[list[InterventionModel]] = relationship(back_populates="participant")


class AgendaModel(Base):
    __tablename__ = "agendas"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    meeting_id: Mapped[str] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    meeting: Mapped[MeetingModel] = relationship(back_populates="agenda")
    items: Mapped[list[AgendaItemModel]] = relationship(back_populates="agenda")


class AgendaItemModel(Base):
    __tablename__ = "agenda_items"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    agenda_id: Mapped[str] = mapped_column(ForeignKey("agendas.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    agenda: Mapped[AgendaModel] = relationship(back_populates="items")
    discussions: Mapped[list[DiscussionModel]] = relationship(back_populates="agenda_item")


class DiscussionModel(Base):
    __tablename__ = "discussions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    meeting_id: Mapped[str] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    agenda_item_id: Mapped[str] = mapped_column(ForeignKey("agenda_items.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    meeting: Mapped[MeetingModel] = relationship(back_populates="discussions")
    agenda_item: Mapped[AgendaItemModel] = relationship(back_populates="discussions")
    interventions: Mapped[list[InterventionModel]] = relationship(back_populates="discussion")
    motions: Mapped[list[MotionModel]] = relationship(back_populates="discussion")


class InterventionModel(Base):
    __tablename__ = "interventions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    discussion_id: Mapped[str] = mapped_column(ForeignKey("discussions.id"), nullable=False)
    participant_id: Mapped[str] = mapped_column(ForeignKey("participants.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    discussion: Mapped[DiscussionModel] = relationship(back_populates="interventions")
    participant: Mapped[ParticipantModel] = relationship(back_populates="interventions")


class MotionModel(Base):
    __tablename__ = "motions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    discussion_id: Mapped[str] = mapped_column(ForeignKey("discussions.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    discussion: Mapped[DiscussionModel] = relationship(back_populates="motions")
    vote: Mapped[VoteModel | None] = relationship(back_populates="motion", uselist=False)
    resolutions: Mapped[list[ResolutionModel]] = relationship(back_populates="motion")


class VoteModel(Base):
    __tablename__ = "votes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    motion_id: Mapped[str] = mapped_column(ForeignKey("motions.id"), nullable=False)
    yes_count: Mapped[int] = mapped_column(nullable=False, default=0)
    no_count: Mapped[int] = mapped_column(nullable=False, default=0)
    abstain_count: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    motion: Mapped[MotionModel] = relationship(back_populates="vote")


class ResolutionModel(Base):
    __tablename__ = "resolutions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    meeting_id: Mapped[str] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    motion_id: Mapped[str] = mapped_column(ForeignKey("motions.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    motion: Mapped[MotionModel] = relationship(back_populates="resolutions")
    actions: Mapped[list[ActionModel]] = relationship(back_populates="resolution")


class ActionModel(Base):
    __tablename__ = "actions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    meeting_id: Mapped[str] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    resolution_id: Mapped[str] = mapped_column(ForeignKey("resolutions.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    resolution: Mapped[ResolutionModel] = relationship(back_populates="actions")


class AttachmentModel(Base):
    __tablename__ = "attachments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    meeting_id: Mapped[str] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    meeting: Mapped[MeetingModel] = relationship(back_populates="attachments")


class BusinessFactModel(Base):
    __tablename__ = "business_facts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=_uuid7)
    meeting_id: Mapped[str] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    meeting: Mapped[MeetingModel] = relationship(back_populates="business_facts")
    references: Mapped[list[BusinessFactReferenceModel]] = relationship(
        back_populates="fact",
        cascade="all, delete-orphan",
        order_by="BusinessFactReferenceModel.position",
    )


class BusinessFactReferenceModel(Base):
    __tablename__ = "business_fact_references"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=_uuid7)
    fact_id: Mapped[str] = mapped_column(ForeignKey("business_facts.id"), nullable=False)
    concept_type: Mapped[str] = mapped_column(String(64), nullable=False)
    concept_id: Mapped[str] = mapped_column(String(64), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    fact: Mapped[BusinessFactModel] = relationship(back_populates="references")


@event.listens_for(BusinessFactModel, "before_update")
def _reject_business_fact_update(mapper, connection, target):
    raise ValueError("BusinessFact row is immutable and append-only; use a new fact record instead.")
