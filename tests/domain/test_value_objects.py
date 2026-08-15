from dataclasses import FrozenInstanceError
from datetime import date, datetime, timedelta

import pytest

from domain.value_objects import (
    DateRange,
    Duration,
    EmailAddress,
    ParticipantRole,
    PersonName,
    PostalAddress,
    TimeInterval,
    VoteCount,
)


def test_person_name_is_trimmed_and_immutable() -> None:
    value = PersonName("  Alice Doe  ")
    assert value.value == "Alice Doe"
    with pytest.raises(FrozenInstanceError):
        value.value = "Changed"  # type: ignore[misc]


def test_person_name_rejects_empty_value() -> None:
    with pytest.raises(ValueError):
        PersonName("   ")


def test_person_name_rejects_non_string_value() -> None:
    with pytest.raises(ValueError):
        PersonName(None)  # type: ignore[arg-type]


def test_email_address_normalizes_and_compares_by_value() -> None:
    first = EmailAddress("User@example.com")
    second = EmailAddress("user@example.com")
    assert first == second
    assert first.value == "user@example.com"


def test_email_address_rejects_invalid_value() -> None:
    with pytest.raises(ValueError):
        EmailAddress("not-an-email")


def test_postal_address_rejects_empty_value() -> None:
    with pytest.raises(ValueError):
        PostalAddress("\n\t")


def test_time_interval_duration_and_validation() -> None:
    start = datetime(2026, 8, 15, 10, 0, 0)
    end = datetime(2026, 8, 15, 10, 30, 0)
    interval = TimeInterval(start=start, end=end)

    assert interval.duration == timedelta(minutes=30)

    with pytest.raises(ValueError):
        TimeInterval(start=end, end=start)


def test_duration_validation_and_seconds_accessor() -> None:
    duration = Duration(timedelta(seconds=90))
    assert duration.seconds == 90

    with pytest.raises(ValueError):
        Duration(timedelta(seconds=-1))


def test_date_range_validation_and_equality() -> None:
    first = DateRange(start=date(2026, 8, 10), end=date(2026, 8, 15))
    second = DateRange(start=date(2026, 8, 10), end=date(2026, 8, 15))
    assert first == second

    with pytest.raises(ValueError):
        DateRange(start=date(2026, 8, 15), end=date(2026, 8, 10))


def test_vote_count_total_and_validation() -> None:
    votes = VoteCount(yes=5, no=2, abstain=1)
    assert votes.total == 8

    with pytest.raises(ValueError):
        VoteCount(yes=-1, no=0)


def test_vote_count_rejects_non_integer_values() -> None:
    with pytest.raises(ValueError):
        VoteCount(yes=1.5, no=0)  # type: ignore[arg-type]

    with pytest.raises(ValueError):
        VoteCount(yes=True, no=0)


def test_participant_role_trimmed_and_rejects_empty() -> None:
    role = ParticipantRole("  Chair  ")
    assert role.value == "Chair"

    with pytest.raises(ValueError):
        ParticipantRole(" ")
