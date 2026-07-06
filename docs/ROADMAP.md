# Roadmap

## MVP

- CLI commands: `doctor`, `validate`, `preview`, `init`, `ingest`, `analyze`, `plan`, `export`.
- External travel project directories created by `travel-film-maker init <directory>`.
- Project-local `.gitignore` that keeps media and generated output out of source control.
- Remote media source data model for Google Photos shared albums.
- Project Model for trip metadata, days, routes, highlights, asset folders, and statistics.
- Style Engine for documentary visual language decisions.
- Asset Engine for folder scanning and basic media type detection.
- Story Engine that emits scenes rather than editor-specific clips.
- Timeline Engine that emits a normalized editor-agnostic timeline.
- Filesystem import for photos and videos.
- Text-only preview output and normalized timeline JSON output.

## v0.2

- Video metadata via `ffprobe`.
- EXIF and GPX pairing.
- Optional thumbnail/preview cache for remote media.
- Ken Burns planning for photos.
- Day-based chapters.
- Chapter cards, route stats, and basic map shots.
- DaVinci exporter consumes normalized timeline.

## v0.3

- Google Photos Takeout import.
- Duplicate and blur detection.
- Scene detection for videos.
- Music rhythm and pacing rules.
- DaVinci Resolve scripting export.

## v0.4

- Plugin API.
- AI-assisted photo selection.
- Voiceover and narration planner.
- Storyboard and shot list generation.
- HTML preview timeline.

## v1.0

- Stable YAML schema.
- Reproducible film builds.
- Test fixtures.
- Documentation for custom styles.
- Official open-source release with a sample project.
