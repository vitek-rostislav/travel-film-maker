# Story Engine

The Story Engine turns the Project Model, Style Profile and scanned assets from an external travel project into documentary scenes.

It should not produce DaVinci clips directly. It produces editor-agnostic scene descriptions with intent, duration hints, metadata and optional assets.

Initial scene vocabulary:

- `chapter_card`
- `map`
- `highlight`
- `road_sequence`
- `place_sequence`
- `reflection`

Current implementation:

- creates one chapter card per day
- creates one map scene when route map data is available
- turns each project highlight into a highlight scene
- applies pacing hints from the Style Engine

Later versions should use GPS movement, media density, scene detection and manual notes to produce stronger narrative structure.
