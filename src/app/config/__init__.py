from __future__ import annotations

import os
from urllib.parse import urlparse


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_database_settings() -> dict[str, object]:
    """Return database connection values without importing SQLAlchemy.

    This keeps the domain and business_facts packages free from persistence
    dependencies while enforcing the environment contract for Phase 2.
    """
    database_url = _require_env("ACTA_DATABASE_URL")
    parsed = urlparse(database_url)

    if parsed.scheme not in {"postgresql", "postgresql+psycopg"}:
        raise ValueError("ACTA_DATABASE_URL must use a PostgreSQL scheme")

    if not parsed.hostname or not parsed.path or parsed.path == "/":
        raise ValueError("ACTA_DATABASE_URL must include host and database")

    return {
        "drivername": parsed.scheme,
        "username": parsed.username or "",
        "password": parsed.password or "",
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "database": parsed.path.lstrip("/"),
    }
