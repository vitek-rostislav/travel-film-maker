# Travel Film Maker

Generate cinematic travel documentaries from photos and videos.

Inspired by Long Way Round.

## Status

This repository currently contains the first modular Python scaffold:

- YAML-based project format.
- CLI commands for project initialization, ingest, analysis, planning, and export.
- Editor-neutral timeline model.
- Initial FCPXML export path for DaVinci Resolve.

## Quick start

```bash
python -m travel_film_maker.cli.main --help
```

When installed as a package:

```bash
tfm init --title "Balkan Road Trip" --timezone Europe/Prague
tfm ingest
tfm analyze
tfm plan
tfm export --format fcpxml
```

During local development without installation:

```bash
PYTHONPATH=src python -m travel_film_maker.cli.main --project-dir ./demo init --title "Demo Trip"
PYTHONPATH=src python -m travel_film_maker.cli.main --project-dir ./demo ingest
PYTHONPATH=src python -m travel_film_maker.cli.main --project-dir ./demo analyze
PYTHONPATH=src python -m travel_film_maker.cli.main --project-dir ./demo plan
PYTHONPATH=src python -m travel_film_maker.cli.main --project-dir ./demo export --format fcpxml
```

## Trip planning

The root `timeline.yaml` can be used as a human-authored trip plan with `project`, `trip`, and `days` sections. When this format is detected, `tfm plan` preserves it and writes the generated edit timeline to `edit_timeline.yaml` instead of overwriting the source plan.

## Planned features

- Google Photos import
- GPS extraction
- Google Earth transitions
- DaVinci Resolve timeline generation
- AI photo selection
- Day statistics
- Ken Burns animation
- Automatic chapter cards
- Soundtrack support
