"""Core domain value objects for the business model."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta

_EMAIL_RE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.IGNORECASE)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True, slots=True)
class PersonName:
    value: str

    def __post_init__(self) -> None:
        normalized = _require_non_empty(self.value, "PersonName.value")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        normalized = _require_non_empty(self.value, "EmailAddress.value")
        if not _EMAIL_RE.match(normalized):
            raise ValueError("EmailAddress.value must be a valid email address")
        object.__setattr__(self, "value", normalized.lower())


@dataclass(frozen=True, slots=True)
class PostalAddress:
    value: str

    def __post_init__(self) -> None:
        normalized = _require_non_empty(self.value, "PostalAddress.value")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class TimeInterval:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValueError("TimeInterval.end must be greater than or equal to start")

    @property
    def duration(self) -> timedelta:
        return self.end - self.start


@dataclass(frozen=True, slots=True)
class Duration:
    value: timedelta

    def __post_init__(self) -> None:
        if self.value < timedelta(0):
            raise ValueError("Duration.value must be non-negative")

    @property
    def seconds(self) -> float:
        return self.value.total_seconds()


@dataclass(frozen=True, slots=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValueError("DateRange.end must be greater than or equal to start")


@dataclass(frozen=True, slots=True)
class VoteCount:
    yes: int
    no: int
    abstain: int = 0

    def __post_init__(self) -> None:
        for field_name in ("yes", "no", "abstain"):
            field_value = getattr(self, field_name)
            if isinstance(field_value, bool) or not isinstance(field_value, int):
                raise ValueError(f"VoteCount.{field_name} must be an integer")
            if field_value < 0:
                raise ValueError(f"VoteCount.{field_name} must be non-negative")

    @property
    def total(self) -> int:
        return self.yes + self.no + self.abstain


@dataclass(frozen=True, slots=True)
class ParticipantRole:
    value: str

    def __post_init__(self) -> None:
        normalized = _require_non_empty(self.value, "ParticipantRole.value")
        object.__setattr__(self, "value", normalized)
