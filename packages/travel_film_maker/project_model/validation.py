from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from travel_film_maker.core.config import load_yaml
from travel_film_maker.project_model.model import ProjectModel, load_project_model


@dataclass(slots=True)
class ValidationResult:
    project: ProjectModel | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_project_file(path: Path) -> ValidationResult:
    result = ValidationResult()
    if not path.exists():
        result.errors.append(f"Project file does not exist: {path}")
        return result

    try:
        data = load_yaml(path)
    except Exception as exc:  # noqa: BLE001 - CLI validation should report parser failures.
        result.errors.append(f"Cannot read project YAML: {exc}")
        return result

    _validate_required_root(data, result)
    _validate_project(data, result)
    _validate_trip(data, result)
    _validate_days(data, path.parent, result)

    if result.ok:
        result.project = load_project_model(path)
    return result


def _validate_required_root(data: dict[str, object], result: ValidationResult) -> None:
    for key in ("project", "trip", "days"):
        if key not in data:
            result.errors.append(f"Missing root section: {key}")


def _validate_project(data: dict[str, object], result: ValidationResult) -> None:
    project = data.get("project")
    if not isinstance(project, dict):
        return
    for key in ("title", "style", "language", "aspect_ratio"):
        if not project.get(key):
            result.errors.append(f"Missing project.{key}")


def _validate_trip(data: dict[str, object], result: ValidationResult) -> None:
    trip = data.get("trip")
    if not isinstance(trip, dict):
        return
    route = trip.get("route", [])
    if not isinstance(route, list) or len(route) < 2:
        result.warnings.append("trip.route should contain at least origin and destination")


def _validate_days(data: dict[str, object], project_dir: Path, result: ValidationResult) -> None:
    days = data.get("days")
    if not isinstance(days, list) or not days:
        result.errors.append("days must contain at least one day/chapter")
        return

    seen_ids: set[str] = set()
    for index, day in enumerate(days, start=1):
        if not isinstance(day, dict):
            result.errors.append(f"days[{index}] must be an object")
            continue

        day_id = str(day.get("id") or f"#{index}")
        if day_id in seen_ids:
            result.errors.append(f"Duplicate day id: {day_id}")
        seen_ids.add(day_id)

        for key in ("id", "date", "title", "route", "assets", "map"):
            if not day.get(key):
                result.errors.append(f"{day_id}: missing {key}")

        highlights = day.get("highlights", [])
        if not isinstance(highlights, list) or not highlights:
            result.warnings.append(f"{day_id}: no highlights defined")

        assets = day.get("assets", {})
        if isinstance(assets, dict) and assets.get("folder"):
            asset_folder = project_dir / str(assets["folder"])
            if not asset_folder.exists():
                result.warnings.append(f"{day_id}: asset folder does not exist yet: {asset_folder}")
