# data/meetings Conventions

This folder stores sample meeting datasets used for local validation.

Dataset folder pattern:

- meeting_<sequence>_<yyyy-mm-dd>_<slug>

Required content for each dataset folder:

- original/
- audio/
- segments/
- knowledge/
- output/
- logs/
- metadata.yaml

Metadata template:

- ../meetings/metadata-template.yaml

Rules:

- Keep processing local and offline.
- Do not modify files under original/ once checksums are registered.
- Add license and provenance evidence in metadata.yaml.
