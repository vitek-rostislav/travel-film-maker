from __future__ import annotations

from pathlib import Path
from typing import Any

from travel_film_maker.core.config import load_yaml


def load_trip_plan(project_dir: Path) -> dict[str, Any] | None:
    for filename in ("trip.yaml", "timeline.yaml"):
        path = project_dir / filename
        if not path.exists():
            continue
        data = load_yaml(path)
        if is_trip_plan(data):
            return data
    return None


def is_trip_plan(data: dict[str, Any]) -> bool:
    return isinstance(data.get("days"), list) and isinstance(data.get("trip"), dict)


def timeline_output_path(project_dir: Path) -> Path:
    timeline_path = project_dir / "timeline.yaml"
    if timeline_path.exists():
        data = load_yaml(timeline_path)
        if is_trip_plan(data):
            return project_dir / "edit_timeline.yaml"
    return timeline_path
