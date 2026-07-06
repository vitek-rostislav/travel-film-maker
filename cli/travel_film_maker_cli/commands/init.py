from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.core.config import dump_yaml
from travel_film_maker.core.project import slugify


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("init", help="Create a new Travel Film Maker project.")
    parser.add_argument("directory", type=Path, help="Directory where the travel project should be created.")
    parser.add_argument("--title", default="Untitled Travel Film", help="Project title.")
    parser.add_argument("--id", default=None, help="Stable project id. Defaults to a slug from title.")
    parser.add_argument("--timezone", default="UTC", help="Project timezone.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    project_dir: Path = args.directory
    project_dir.mkdir(parents=True, exist_ok=True)

    for child in ("assets/day01", "gps", "music", "output", "cache", "renders"):
        (project_dir / child).mkdir(parents=True, exist_ok=True)

    project = _default_project_model(title=args.title)
    dump_yaml(project_dir / "project.yaml", project)
    dump_yaml(project_dir / "style.yaml", _default_style_model())
    (project_dir / ".gitignore").write_text(_project_gitignore(), encoding="utf-8")

    print(f"Initialized Travel Film Maker project in {project_dir}")
    return 0


def _default_project_model(title: str) -> dict[str, object]:
    return {
        "project": {
            "id": slugify(title),
            "title": title,
            "style": "long-way-round-inspired",
            "language": "en",
            "aspect_ratio": "16:9",
        },
        "trip": {
            "totals": {},
            "route": ["Start", "Destination"],
        },
        "media_sources": [
            {
                "id": "local_assets",
                "type": "local_folder",
                "path": "assets",
                "mapping": {
                    "default_day_strategy": "folder",
                    "fallback_day_strategy": "manual",
                },
            }
        ],
        "days": [
            {
                "id": "day01",
                "date": "2026-01-01",
                "title": "Day 1",
                "location": "Destination",
                "route": "Start -> Destination",
                "country_flags": [],
                "stats": {},
                "highlights": ["First travel day"],
                "assets": {"folder": "assets/day01"},
                "media": {
                    "source": "local_assets",
                    "filters": {"folder": "day01"},
                },
                "map": {"type": "route", "from": "Start", "to": "Destination"},
                "mood": "departure",
            }
        ],
    }


def _default_style_model() -> dict[str, object]:
    return {
        "style": {
            "name": "long-way-round-inspired",
            "chapter_card": {"layout": "location-date-statistics", "tone": "documentary"},
            "map_style": {"type": "earth-route", "labels": "places-and-borders"},
            "typography": {"title": "condensed-bold", "body": "clean-sans"},
            "transitions": {"default": "straight-cut", "chapter": "map-wipe"},
            "pacing": {"photo_seconds": 5, "video_seconds": 6, "map_seconds": 7, "chapter_seconds": 4},
            "ken_burns": {"enabled": True, "intensity": "restrained"},
            "subtitles": {"placement": "lower-third", "tone": "documentary"},
        }
    }


def _project_gitignore() -> str:
    return """# Personal media and generated output
assets/
output/
cache/
renders/
.travel-film-maker-cache/

# Temporary files
*.tmp
*.temp
*.log
.DS_Store
Thumbs.db

# DaVinci Resolve cache
CacheClip/
OptimizedMedia/
ProxyMedia/
.gallery/

# Google Earth Studio temporary files
earth-studio-cache/
google-earth-studio/
*.esp
*.esp.json
"""
