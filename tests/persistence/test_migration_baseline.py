from __future__ import annotations

import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import pytest


@pytest.mark.skipif(not os.getenv("ACTA_TEST_DATABASE_URL"), reason="requires ACTA_TEST_DATABASE_URL")
def test_alembic_upgrade_and_downgrade_on_disposable_database() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    base_url = os.environ["ACTA_TEST_DATABASE_URL"]
    psql_base_url = base_url.replace("postgresql+psycopg://", "postgresql://", 1)
    parsed = urlparse(psql_base_url)
    temp_db = f"acta_cd_alembic_{os.getpid()}_{hash(base_url)}"
    temp_db = temp_db.replace("-", "_")

    admin_url = parsed._replace(path="/postgres")
    admin_dsn = urlunparse(admin_url)
    temp_dsn = parsed._replace(path=f"/{temp_db}")
    temp_url = urlunparse(temp_dsn).replace("postgresql://", "postgresql+psycopg://", 1)

    try:
        subprocess.run(
            ["psql", admin_dsn, "-v", "ON_ERROR_STOP=1", "-c", f"CREATE DATABASE \"{temp_db}\";"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )

        env = os.environ.copy()
        env["ACTA_DATABASE_URL"] = temp_url
        subprocess.run(
            ["uv", "run", "alembic", "-c", str(repo_root / "alembic.ini"), "upgrade", "head"],
            check=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        subprocess.run(
            ["uv", "run", "alembic", "-c", str(repo_root / "alembic.ini"), "current"],
            check=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        subprocess.run(
            ["uv", "run", "alembic", "-c", str(repo_root / "alembic.ini"), "downgrade", "base"],
            check=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    finally:
        subprocess.run(
            ["psql", admin_dsn, "-v", "ON_ERROR_STOP=1", "-c", f"DROP DATABASE IF EXISTS \"{temp_db}\";"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )
