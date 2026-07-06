# Architecture

Travel Film Maker is a reusable framework. It is not a place to store trips.

## Repository Boundary

The framework repository contains code, schemas, documentation and tests:

```text
travel-film-maker/
  packages/
  cli/
  exporters/
  docs/
  schemas/
  tests/
  README.md
```

Travel projects are external directories:

```text
~/Movies/Europe2026/
  project.yaml
  style.yaml
  assets/
    day01/
    day02/
  gps/
  music/
  output/
```

Personal media, GPS tracks, music, generated output and editor caches never belong in the framework repository.

External project repositories should use their generated `.gitignore` to exclude media and generated artifacts. Personal photos and videos should stay in local folders or remote media providers.

## Data Flow

```text
external project directory
  -> Project Model
  -> Style Engine
  -> Asset Engine
  -> Story Engine
  -> Timeline Engine
  -> Exporters
```

The framework is not `YAML -> DaVinci Resolve`. DaVinci Resolve is only one exporter.

## Project Model

`project.yaml` describes the trip:

- high-level metadata
- days and chapters
- routes
- highlights
- asset folders
- statistics

The Project Model is loaded from an external project directory passed to the CLI.

## Style Engine

`style.yaml` describes the visual language:

- chapter card layout
- map style
- typography
- transitions
- pacing
- Ken Burns behavior
- subtitle style

If `style.yaml` is missing, the framework falls back to defaults based on `project.yaml`.

## Asset Engine

The Asset Engine reads media references from the external project.

Supported source types in the data model:

- `google_photos_shared_album`
- `local_folder`
- `google_drive`
- `icloud_export`
- `dropbox`
- `onedrive`

Only local folders are scanned today. Google Photos shared albums are treated as remote references; the framework does not download photos or videos by default.

Optional downloaded thumbnails/previews should be stored in the project-local ignored cache, never in the framework repository.

## Story Engine

The Story Engine converts project data, style and assets into documentary scenes. It produces scenes with intent and duration hints, not editor-specific clips.

## Timeline Engine

The Timeline Engine converts scenes into a normalized internal timeline containing timeline items, titles, maps, transitions, durations and camera movement metadata.

## Exporters

Exporters consume the normalized timeline model. Planned targets include:

- DaVinci Resolve
- Premiere
- CapCut
- FFmpeg

Exporters must not own story logic.

## CLI Contract

All project-facing commands accept an external project directory or `.`:

```bash
travel-film-maker init ~/Movies/Europe2026
travel-film-maker validate ~/Movies/Europe2026
travel-film-maker preview .
travel-film-maker render /path/to/project
```

`render` currently writes normalized planning data only. Video rendering is intentionally out of scope for this phase.
