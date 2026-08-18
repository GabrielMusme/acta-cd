from __future__ import annotations

import os
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from business_facts.models import BusinessFactCategory
from infrastructure.persistence.models import (
    Base,
    BusinessFactModel,
    BusinessFactReferenceModel,
    MeetingModel,
    OrganizationModel,
)


@pytest.mark.skipif(not os.getenv("ACTA_DATABASE_URL"), reason="requires ACTA_DATABASE_URL")
def test_business_fact_roundtrip_persists_fact_and_references() -> None:
    engine = create_engine(os.environ["ACTA_DATABASE_URL"], future=True)
    Base.metadata.create_all(engine)
    now = datetime.now(timezone.utc)

    try:
        with Session(engine) as session:
            session.add(
                OrganizationModel(
                    id="org-01",
                    name="Example Org",
                    created_at=now,
                    updated_at=now,
                )
            )
            session.add(
                MeetingModel(
                    id="meeting-01",
                    organization_id="org-01",
                    status="created",
                    created_at=now,
                    updated_at=now,
                )
            )
            session.commit()

        fact = BusinessFactModel(
            id="fact-01",
            meeting_id="meeting-01",
            category=BusinessFactCategory.BF_001_MEETING_CREATED.value,
            occurred_at=now,
            payload={"source": "unit-test", "meeting_title": "Kickoff"},
            references=[
                BusinessFactReferenceModel(
                    fact_id="fact-01",
                    concept_type="Organization",
                    concept_id="org-01",
                    position=0,
                ),
                BusinessFactReferenceModel(
                    fact_id="fact-01",
                    concept_type="Meeting",
                    concept_id="meeting-01",
                    position=1,
                ),
            ],
        )

        with Session(engine) as session:
            session.add(fact)
            session.commit()

        with Session(engine) as session:
            row = session.get(BusinessFactModel, "fact-01")
            assert row is not None
            assert row.meeting_id == "meeting-01"
            assert row.category == BusinessFactCategory.BF_001_MEETING_CREATED.value
            assert row.payload["source"] == "unit-test"
            assert [ref.concept_type for ref in row.references] == ["Organization", "Meeting"]
            assert [ref.concept_id for ref in row.references] == ["org-01", "meeting-01"]
    finally:
        Base.metadata.drop_all(engine)


@pytest.mark.skipif(not os.getenv("ACTA_DATABASE_URL"), reason="requires ACTA_DATABASE_URL")
def test_business_fact_updates_are_rejected_as_append_only() -> None:
    engine = create_engine(os.environ["ACTA_DATABASE_URL"], future=True)
    Base.metadata.create_all(engine)
    now = datetime.now(timezone.utc)

    try:
        with Session(engine) as session:
            session.add(
                OrganizationModel(
                    id="org-02",
                    name="Example Org 2",
                    created_at=now,
                    updated_at=now,
                )
            )
            session.add(
                MeetingModel(
                    id="meeting-02",
                    organization_id="org-02",
                    status="created",
                    created_at=now,
                    updated_at=now,
                )
            )
            session.add(
                BusinessFactModel(
                    id="fact-02",
                    meeting_id="meeting-02",
                    category=BusinessFactCategory.BF_001_MEETING_CREATED.value,
                    occurred_at=now,
                    payload={"source": "unit-test"},
                    references=[
                        BusinessFactReferenceModel(
                            fact_id="fact-02",
                            concept_type="Meeting",
                            concept_id="meeting-02",
                            position=0,
                        )
                    ],
                )
            )
            session.commit()

        with Session(engine) as session:
            row = session.get(BusinessFactModel, "fact-02")
            assert row is not None
            row.category = BusinessFactCategory.BF_002_MEETING_STARTED.value
            with pytest.raises(ValueError, match="immutable and append-only"):
                session.commit()
    finally:
        Base.metadata.drop_all(engine)
