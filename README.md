# Travel Film Maker

Travel Film Maker is an open-source framework for building cinematic travel documentaries from external project folders containing trip metadata, photos, videos, GPS data and music.

This repository contains only the framework. It must not contain personal travel projects, photos, videos, music, GPS tracks or rendered output.

## Framework vs Travel Project

The framework is this repository:

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

A travel project lives outside this repository, for example:

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

The framework reads a travel project directory and produces editor-agnostic planning data. Exporters can later translate that data for DaVinci Resolve, Premiere, CapCut, FFmpeg or other tools.

## Create A Project

```bash
travel-film-maker init ~/Movies/Europe2026 --title "Europe 2026"
```

This creates:

- `project.yaml`
- `style.yaml`
- `assets/`
- `gps/`
- `music/`
- `output/`
- a project-local `.gitignore`

The generated project `.gitignore` excludes personal media and generated files from that project repository.

## Work With A Project

From anywhere:

```bash
travel-film-maker validate ~/Movies/Europe2026
travel-film-maker preview ~/Movies/Europe2026
travel-film-maker render ~/Movies/Europe2026
```

From inside a project:

```bash
cd ~/Movies/Europe2026
travel-film-maker validate .
travel-film-maker preview .
travel-film-maker render .
```

`render` currently builds a normalized timeline JSON in `output/`. It does not render video yet.

## Development

```bash
python -m pip install -e ".[dev]"
travel-film-maker doctor
python -m pytest
```

The framework repository `.gitignore` is intentionally limited to local development files. User media belongs in external travel project directories, never in this repository.
