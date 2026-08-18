import importlib
import os

import pytest


@pytest.mark.parametrize(
    "module_name",
    ["domain", "business_facts"],
)
def test_domain_and_business_fact_modules_import_without_persistence_dependency(module_name: str) -> None:
    importlib.import_module(module_name)


def test_database_settings_require_env_url(monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib

    monkeypatch.delenv("ACTA_DATABASE_URL", raising=False)
    module = importlib.import_module("app.config")
    with pytest.raises(ValueError, match="ACTA_DATABASE_URL"):
        module.get_database_settings()


def test_database_settings_accept_valid_env_url(monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib

    monkeypatch.setenv("ACTA_DATABASE_URL", "postgresql+psycopg://app_user:secret@localhost:5432/acta_cd")
    module = importlib.import_module("app.config")

    settings = module.get_database_settings()

    assert settings["drivername"] == "postgresql+psycopg"
    assert settings["username"] == "app_user"
    assert settings["database"] == "acta_cd"
    assert settings["host"] == "localhost"
    assert settings["port"] == 5432
