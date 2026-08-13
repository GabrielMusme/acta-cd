"""Smoke imports for P0-T01 skeleton."""

import importlib

MODULES = [
    "app",
    "app.main",
    "domain",
    "domain.entities",
    "domain.value_objects",
    "domain.events",
    "domain.repositories",
    "domain.services",
    "business_facts",
    "business_facts.models",
    "business_facts.services",
    "business_facts.validators",
    "knowledge",
    "knowledge.models",
    "knowledge.services",
    "knowledge.evaluators",
    "knowledge.exporters",
    "processing",
    "processing.ingestion",
    "processing.transcription",
    "processing.diarization",
    "processing.segmentation",
    "processing.extraction",
    "processing.validation",
    "processing.checkpoints",
    "processing.workers",
    "infrastructure",
    "infrastructure.persistence",
    "infrastructure.repositories",
    "infrastructure.storage",
    "infrastructure.logging",
    "shared",
    "shared.schemas",
    "shared.utils",
    "shared.errors",
]


def test_base_packages_importable() -> None:
    for module_name in MODULES:
        importlib.import_module(module_name)
