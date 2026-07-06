from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from travel_film_maker.core.config import load_yaml
from travel_film_maker.project_model.model import ProjectModel


@dataclass(slots=True)
class StyleProfile:
    name: str
    chapter_card: dict[str, str]
    map_style: dict[str, str]
    typography: dict[str, str]
    transitions: dict[str, str]
    pacing: dict[str, int]
    ken_burns: dict[str, object]
    subtitles: dict[str, str]


def build_style_profile(project: ProjectModel) -> StyleProfile:
    if project.style in {"long-way-round", "long-way-round-inspired"}:
        return StyleProfile(
            name=project.style,
            chapter_card={"layout": "location-date-statistics", "tone": "documentary"},
            map_style={"type": "earth-route", "labels": "places-and-borders"},
            typography={"title": "condensed-bold", "body": "clean-sans"},
            transitions={"default": "straight-cut", "chapter": "map-wipe"},
            pacing={"photo_seconds": 5, "video_seconds": 6, "map_seconds": 7, "chapter_seconds": 4},
            ken_burns={"enabled": True, "intensity": "restrained"},
            subtitles={"placement": "lower-third", "tone": "documentary"},
        )

    return StyleProfile(
        name=project.style,
        chapter_card={"layout": "simple-title", "tone": "neutral"},
        map_style={"type": "flat-route", "labels": "major-places"},
        typography={"title": "bold-sans", "body": "sans"},
        transitions={"default": "straight-cut", "chapter": "fade"},
        pacing={"photo_seconds": 5, "video_seconds": 6, "map_seconds": 6, "chapter_seconds": 4},
        ken_burns={"enabled": True, "intensity": "medium"},
        subtitles={"placement": "lower-third", "tone": "neutral"},
    )


def load_style_profile(project: ProjectModel) -> StyleProfile:
    style_path = project.root_dir / "style.yaml"
    if not style_path.exists():
        return build_style_profile(project)

    data = load_yaml(style_path)
    style = data.get("style", {})
    base = build_style_profile(project)
    return StyleProfile(
        name=str(style.get("name", base.name)),
        chapter_card=_merged(base.chapter_card, style.get("chapter_card")),
        map_style=_merged(base.map_style, style.get("map_style")),
        typography=_merged(base.typography, style.get("typography")),
        transitions=_merged(base.transitions, style.get("transitions")),
        pacing=_merged(base.pacing, style.get("pacing")),
        ken_burns=_merged(base.ken_burns, style.get("ken_burns")),
        subtitles=_merged(base.subtitles, style.get("subtitles")),
    )


def _merged(defaults: dict[str, Any], overrides: object) -> dict[str, Any]:
    if not isinstance(overrides, dict):
        return dict(defaults)
    merged = dict(defaults)
    merged.update(overrides)
    return merged
