"""Typed invariant errors for domain invariant validation."""

from __future__ import annotations


class DomainInvariantError(ValueError):
    """Base error for domain invariant violations."""

    invariant_id: str = "DMI-000"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"{self.invariant_id}: {message}")


class DMI001Error(DomainInvariantError):
    invariant_id = "DMI-001"


class DMI002Error(DomainInvariantError):
    invariant_id = "DMI-002"


class DMI003Error(DomainInvariantError):
    invariant_id = "DMI-003"


class DMI004Error(DomainInvariantError):
    invariant_id = "DMI-004"


class DMI005Error(DomainInvariantError):
    invariant_id = "DMI-005"


class DMI006Error(DomainInvariantError):
    invariant_id = "DMI-006"


class DMI007Error(DomainInvariantError):
    invariant_id = "DMI-007"


class DMI008Error(DomainInvariantError):
    invariant_id = "DMI-008"


class DMI009Error(DomainInvariantError):
    invariant_id = "DMI-009"


class DMI010Error(DomainInvariantError):
    invariant_id = "DMI-010"


class DMI011Error(DomainInvariantError):
    invariant_id = "DMI-011"


class DMI012Error(DomainInvariantError):
    invariant_id = "DMI-012"


class DMI013Error(DomainInvariantError):
    invariant_id = "DMI-013"


class DMI014Error(DomainInvariantError):
    invariant_id = "DMI-014"


class DMI015Error(DomainInvariantError):
    invariant_id = "DMI-015"
