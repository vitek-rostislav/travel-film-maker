from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from travel_film_maker.core.config import load_yaml


@dataclass(slots=True)
class Route:
    label: str
    map: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Day:
    id: str
    date: str
    title: str
    location: str
    route: Route
    highlights: list[str]
    asset_folder: str
    statistics: dict[str, Any] = field(default_factory=dict)
    mood: str | None = None
    country_flags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ProjectModel:
    path: Path
    title: str
    subtitle: str | None
    style: str
    language: str
    aspect_ratio: str
    totals: dict[str, Any]
    route: list[str]
    days: list[Day]

    @property
    def root_dir(self) -> Path:
        return self.path.parent


def load_project_model(path: Path) -> ProjectModel:
    data = load_yaml(path)
    return project_model_from_dict(path, data)


def project_model_from_dict(path: Path, data: dict[str, Any]) -> ProjectModel:
    project = data.get("project", {})
    trip = data.get("trip", {})
    days = [_day_from_dict(day) for day in data.get("days", [])]

    return ProjectModel(
        path=path,
        title=str(project.get("title", "Untitled Travel Film")),
        subtitle=project.get("subtitle"),
        style=str(project.get("style", "documentary-roadtrip")),
        language=str(project.get("language", "en")),
        aspect_ratio=str(project.get("aspect_ratio", "16:9")),
        totals=dict(trip.get("totals") or {}),
        route=[str(item) for item in trip.get("route", [])],
        days=days,
    )


def _day_from_dict(data: dict[str, Any]) -> Day:
    assets = data.get("assets", {})
    return Day(
        id=str(data["id"]),
        date=str(data["date"]),
        title=str(data["title"]),
        location=str(data.get("location", "")),
        route=Route(label=str(data.get("route", "")), map=dict(data.get("map") or {})),
        highlights=[str(item) for item in data.get("highlights", [])],
        asset_folder=str(assets.get("folder", "")),
        statistics=dict(data.get("stats") or {}),
        mood=data.get("mood"),
        country_flags=[str(item) for item in data.get("country_flags", [])],
    )
