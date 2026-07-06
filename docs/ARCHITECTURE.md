# Travel Film Maker Architecture

## Goal

Travel Film Maker is an open-source tool that turns photos, videos, and GPS data into a documentary travel film inspired by road-trip series such as Long Way Round.

The project should stay modular and editor-agnostic internally, while supporting export to DaVinci Resolve as a primary workflow.

## Core Principle

The application should be built as a pipeline:

```text
import -> normalize -> analyze -> story -> edit plan -> export
```

The internal output should not be a DaVinci-specific timeline. It should be a neutral edit decision model that can later be exported to DaVinci Resolve, FCPXML, EDL, JSON, or a preview renderer.

## Directory Structure

```text
travel-film-maker/
  pyproject.toml
  README.md
  docs/
    ARCHITECTURE.md
    ROADMAP.md
    STYLEGUIDE.md
    STORYBOARD.md
    DAVINCI_EXPORT.md

  src/travel_film_maker/
    cli/
      main.py
      commands/
        init.py
        ingest.py
        analyze.py
        plan.py
        export.py

    core/
      project.py
      asset.py
      timeline.py
      story.py
      config.py
      errors.py

    ingest/
      filesystem.py
      google_photos.py
      gopro.py
      gpx.py
      exif.py

    analysis/
      media_probe.py
      gps_matcher.py
      quality_score.py
      duplicate_detector.py
      scene_detector.py
      face_blur_detector.py

    story/
      trip_segmentation.py
      chapter_builder.py
      beat_generator.py
      narration_planner.py
      stats_builder.py

    edit/
      selector.py
      pacing.py
      transitions.py
      ken_burns.py
      music_sync.py
      markers.py

    geo/
      route.py
      geocoding.py
      elevation.py
      map_shots.py

    export/
      opentimelineio.py
      davinci/
        fcpxml.py
        resolve_script.py
        project_template.py
      edl.py
      preview.py

    plugins/
      base.py
      registry.py

  schemas/
    project.schema.json
    asset.schema.json
    timeline.schema.json

  examples/
    europe-trip/
      project.yaml
      assets.yaml
      story.yaml
      timeline.yaml

  tests/
    unit/
    integration/
    fixtures/

  scripts/
    dev_ingest_sample.py
```

## Data Model

YAML should be the public, human-editable project format. SQLite or another local cache can be used internally for indexing and performance.

### project.yaml

```yaml
version: 1
project:
  id: "balkan-2025"
  title: "Balkan Road Trip 2025"
  timezone: "Europe/Prague"
  language: "cs"
  style: "long-way-round-inspired"

sources:
  media:
    - path: "./media/photos"
    - path: "./media/videos"
  gps:
    - path: "./gps/track.gpx"

output:
  fps: 25
  resolution: "3840x2160"
  aspect_ratio: "16:9"
  davinci:
    export_mode: "fcpxml"
    timeline_name: "Balkan Road Trip - Assembly"

style:
  pacing: "documentary"
  photo_motion: "ken_burns"
  chapter_cards: true
  map_transitions: true
  voiceover: true
```

### assets.yaml

```yaml
assets:
  - id: "img_0001"
    type: "photo"
    path: "./media/photos/IMG_0001.jpg"
    captured_at: "2025-06-14T09:32:12+02:00"
    location:
      lat: 46.0569
      lon: 14.5058
      name: "Ljubljana"
    technical:
      width: 4032
      height: 3024
      rating: 0.84
    tags: ["city", "morning", "establishing"]

  - id: "vid_0007"
    type: "video"
    path: "./media/videos/GX010007.MP4"
    captured_at: "2025-06-14T15:10:00+02:00"
    duration: 42.6
    location:
      lat: 45.8150
      lon: 15.9819
    tags: ["road", "motorbike", "movement"]
```

### story.yaml

```yaml
trip:
  start: "2025-06-14"
  end: "2025-06-27"

chapters:
  - id: "day-01"
    title: "Leaving Home"
    date: "2025-06-14"
    route:
      from: "Prague"
      to: "Ljubljana"
      distance_km: 705
    intent: "opening, departure, first road rhythm"
    beats:
      - type: "chapter_card"
      - type: "map_route"
      - type: "establishing"
      - type: "road_sequence"
      - type: "evening_reflection"
```

### timeline.yaml

```yaml
timeline:
  fps: 25
  tracks:
    video:
      - id: "v1"
        clips:
          - asset_id: "img_0001"
            start: "00:00:08:00"
            duration: "00:00:05:00"
            effect:
              type: "ken_burns"
              from: [0.1, 0.1, 0.8, 0.8]
              to: [0.0, 0.0, 1.0, 1.0]

          - type: "generated_map"
            route_id: "day-01"
            start: "00:00:13:00"
            duration: "00:00:07:00"

    audio:
      - id: "a1"
        clips:
          - type: "music"
            path: "./music/main-theme.wav"
            start: "00:00:00:00"
```

## Modules

### ingest

Loads photos, videos, GPX tracks, Google Photos exports, EXIF metadata, and video metadata.

### analysis

Computes asset quality, detects duplicates, estimates sharpness, reads orientation and duration, matches GPS data, finds time gaps, detects scenes, and evaluates basic usability.

### story

Splits the journey into days, chapters, and story beats. This layer creates documentary structure: departure, road movement, problem, pause, landscape, city, and reflection.

### edit

Selects concrete assets, defines pacing, clip durations, Ken Burns movement, map transitions, chapter cards, subtitles, statistics, and markers.

### geo

Works with routes, elevation, distances, places, and data for animated map shots.

### export

Generates OpenTimelineIO as an intermediate timeline format and exports it to FCPXML, EDL, DaVinci Resolve scripts, or preview formats.

### plugins

Provides extension points for importers, scoring models, map renderers, and exporters.

## DaVinci Resolve Export

The practical export path should be:

1. Generate an internal OpenTimelineIO timeline.
2. Export FCPXML for reliable timeline import into Resolve.
3. Generate a Resolve Python script to create projects, bins, markers, marker colors, metadata, and optional setup.
4. Later add project templates, LUT handling, Fusion title templates, and map transition templates.

DaVinci Resolve should be treated as an export backend, not as the internal data model.

## Roadmap

### MVP

- CLI commands: `init`, `ingest`, `analyze`, `plan`, `export`.
- Filesystem import for photos and videos.
- EXIF and GPX pairing.
- YAML files for project, assets, story, and timeline data.
- Basic best-photo selection by day.
- FCPXML export for DaVinci Resolve.

### v0.2

- Video metadata via `ffprobe`.
- Ken Burns planning for photos.
- Day-based chapters.
- Chapter cards, route stats, and basic map shots.
- SQLite cache.

### v0.3

- Google Photos Takeout import.
- Duplicate and blur detection.
- Scene detection for videos.
- Music rhythm and pacing rules.
- DaVinci Resolve scripting export.

### v0.4

- Plugin API.
- AI-assisted photo selection.
- Voiceover and narration planner.
- Storyboard and shot list generation.
- HTML preview timeline.

### v1.0

- Stable YAML schema.
- Reproducible film builds.
- Test fixtures.
- Documentation for custom styles.
- Official open-source release with a sample project.

## Key Decision

The most important architectural choice is to keep DaVinci Resolve as an export backend rather than the internal data model. This keeps the project modular, testable, and portable across editing workflows.
