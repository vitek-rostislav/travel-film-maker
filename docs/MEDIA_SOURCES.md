# Media Sources

Travel Film Maker projects can reference media without committing it to Git.

## Principle

Personal photos, videos, music and GPS tracks should stay outside source control.

The framework repository contains only code and documentation. A travel project can reference local or remote media sources through `project.yaml`.

## Google Photos Shared Album

Initial data model:

```yaml
media_sources:
  - id: google_photos_main
    type: google_photos_shared_album
    url: "https://photos.app.goo.gl/..."
    mapping:
      default_day_strategy: exif_date
      fallback_day_strategy: manual

days:
  - id: day01
    title: "Ostrava -> Vienna"
    media:
      source: google_photos_main
      filters:
        date: "2026-06-27"
        tags:
          - vienna
          - departure
```

Current implementation only validates and previews this data. It does not download from Google Photos.

## Cache

Generated travel projects include ignored cache directories:

```text
cache/
.travel-film-maker-cache/
```

These are intended for future optional thumbnails, metadata snapshots or preview downloads. They should not be committed.

## Future Providers

Planned providers:

- local folder
- Google Drive
- iCloud export
- Dropbox
- OneDrive
