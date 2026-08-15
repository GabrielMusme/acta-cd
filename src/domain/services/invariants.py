"""Domain invariant validation service."""

from __future__ import annotations

from dataclasses import dataclass, field

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
from domain.services.invariant_errors import (
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
    DomainInvariantError,
)


@dataclass(frozen=True, slots=True)
class IdentitySnapshot:
    entity_type: str
    initial_id: str
    current_id: str


@dataclass(frozen=True, slots=True)
class BusinessFactRecord:
    meeting_id: str
    immutable: bool = True
    rewrite_count: int = 0


@dataclass(slots=True)
class DomainInvariantContext:
    meetings: list[Meeting] = field(default_factory=list)
    persons: list[Person] = field(default_factory=list)
    participants: list[Participant] = field(default_factory=list)
    discussions: list[Discussion] = field(default_factory=list)
    motions: list[Motion] = field(default_factory=list)
    votes: list[Vote] = field(default_factory=list)
    resolutions: list[Resolution] = field(default_factory=list)
    actions: list[Action] = field(default_factory=list)
    business_facts: list[BusinessFactRecord] = field(default_factory=list)
    value_objects: list[object] = field(default_factory=list)
    identity_snapshots: list[IdentitySnapshot] = field(default_factory=list)
    history_rewritten: bool = False
    processing_concepts: list[str] = field(default_factory=list)
    knowledge_redefinitions: list[str] = field(default_factory=list)
    human_artifact_inputs: list[str] = field(default_factory=list)


class DomainInvariantValidator:
    """Validates domain invariants DMI-001..DMI-015."""

    def validate_all(self, context: DomainInvariantContext) -> None:
        for validator in self._validators():
            validator(context)

    def validate_and_collect(self, context: DomainInvariantContext) -> list[DomainInvariantError]:
        errors: list[DomainInvariantError] = []
        for validator in self._validators():
            try:
                validator(context)
            except DomainInvariantError as exc:
                errors.append(exc)
        return errors

    def _validators(self) -> tuple:
        return (
            self._validate_dmi_001,
            self._validate_dmi_002,
            self._validate_dmi_003,
            self._validate_dmi_004,
            self._validate_dmi_005,
            self._validate_dmi_006,
            self._validate_dmi_007,
            self._validate_dmi_008,
            self._validate_dmi_009,
            self._validate_dmi_010,
            self._validate_dmi_011,
            self._validate_dmi_012,
            self._validate_dmi_013,
            self._validate_dmi_014,
            self._validate_dmi_015,
        )

    @staticmethod
    def _validate_dmi_001(context: DomainInvariantContext) -> None:
        for value_object in context.value_objects:
            if hasattr(value_object, "id"):
                raise DMI001Error("Value Objects must not possess identity")

    @staticmethod
    def _validate_dmi_002(context: DomainInvariantContext) -> None:
        for snapshot in context.identity_snapshots:
            if snapshot.initial_id != snapshot.current_id:
                details = (
                    f"Identity changed for {snapshot.entity_type}: "
                    f"{snapshot.initial_id} -> {snapshot.current_id}"
                )
                raise DMI002Error(details)

    @staticmethod
    def _validate_dmi_003(context: DomainInvariantContext) -> None:
        for fact in context.business_facts:
            if not fact.immutable:
                raise DMI003Error("Business Facts must be immutable")

    @staticmethod
    def _validate_dmi_004(context: DomainInvariantContext) -> None:
        if context.history_rewritten:
            raise DMI004Error("Historical records must never be rewritten")
        for fact in context.business_facts:
            if fact.rewrite_count > 0:
                raise DMI004Error("Historical records must never be rewritten")

    @staticmethod
    def _validate_dmi_005(context: DomainInvariantContext) -> None:
        closed_meeting_ids = {meeting.id for meeting in context.meetings if meeting.is_closed}
        for participant in context.participants:
            if participant.meeting_id in closed_meeting_ids and not participant.person_id:
                raise DMI005Error("Historical Participants must remain valid after Meeting closure")

    @staticmethod
    def _validate_dmi_006(context: DomainInvariantContext) -> None:
        person_ids = {person.id for person in context.persons}
        for participant in context.participants:
            if participant.person_id not in person_ids:
                raise DMI006Error("Every Participant must reference exactly one Person")

    @staticmethod
    def _validate_dmi_007(context: DomainInvariantContext) -> None:
        meeting_ids = {meeting.id for meeting in context.meetings}
        for participant in context.participants:
            if participant.meeting_id not in meeting_ids:
                raise DMI007Error("Every Participant must belong to exactly one Meeting")

    @staticmethod
    def _validate_dmi_008(context: DomainInvariantContext) -> None:
        meeting_ids = {meeting.id for meeting in context.meetings}
        for discussion in context.discussions:
            if discussion.meeting_id not in meeting_ids:
                raise DMI008Error("Every Discussion must belong to exactly one Meeting")

    @staticmethod
    def _validate_dmi_009(context: DomainInvariantContext) -> None:
        discussion_ids = {discussion.id for discussion in context.discussions}
        for motion in context.motions:
            if motion.discussion_id not in discussion_ids:
                raise DMI009Error("Every Motion must belong to exactly one Discussion")

    @staticmethod
    def _validate_dmi_010(context: DomainInvariantContext) -> None:
        motion_ids = {motion.id for motion in context.motions}
        for vote in context.votes:
            if vote.motion_id not in motion_ids:
                raise DMI010Error("Every Vote must belong to exactly one Motion")

    @staticmethod
    def _validate_dmi_011(context: DomainInvariantContext) -> None:
        resolution_ids = {resolution.id for resolution in context.resolutions}
        for action in context.actions:
            if action.resolution_id not in resolution_ids:
                raise DMI011Error("Every Action must originate from exactly one Resolution")

    @staticmethod
    def _validate_dmi_012(context: DomainInvariantContext) -> None:
        meeting_ids = {meeting.id for meeting in context.meetings}
        for fact in context.business_facts:
            if fact.meeting_id not in meeting_ids:
                raise DMI012Error("Every Business Fact must belong to exactly one Meeting")

    @staticmethod
    def _validate_dmi_013(context: DomainInvariantContext) -> None:
        if context.processing_concepts:
            raise DMI013Error("Processing concepts must not appear in the Business Domain")

    @staticmethod
    def _validate_dmi_014(context: DomainInvariantContext) -> None:
        if context.knowledge_redefinitions:
            raise DMI014Error("Knowledge interpretations must not redefine business concepts")

    @staticmethod
    def _validate_dmi_015(context: DomainInvariantContext) -> None:
        if context.human_artifact_inputs:
            raise DMI015Error("Human-readable artifacts must not be treated as business reality")
