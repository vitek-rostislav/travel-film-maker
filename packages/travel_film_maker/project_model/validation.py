from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from travel_film_maker.core.config import load_yaml
from travel_film_maker.project_model.model import ProjectModel, load_project_model

SUPPORTED_MEDIA_SOURCE_TYPES = {
    "google_photos_shared_album",
    "local_folder",
    "google_drive",
    "icloud_export",
    "dropbox",
    "onedrive",
}


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
    media_sources = _validate_media_sources(data, result)
    _validate_days(data, path.parent, result)
    _validate_day_media(data, media_sources, result)

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


def _validate_media_sources(data: dict[str, object], result: ValidationResult) -> set[str]:
    raw_sources = data.get("media_sources", [])
    if raw_sources in (None, []):
        return set()
    if not isinstance(raw_sources, list):
        result.errors.append("media_sources must be a list")
        return set()

    source_ids: set[str] = set()
    for index, source in enumerate(raw_sources, start=1):
        if not isinstance(source, dict):
            result.errors.append(f"media_sources[{index}] must be an object")
            continue

        source_id = source.get("id")
        source_type = source.get("type")
        if not source_id:
            result.errors.append(f"media_sources[{index}]: missing id")
            continue
        if str(source_id) in source_ids:
            result.errors.append(f"Duplicate media source id: {source_id}")
        source_ids.add(str(source_id))

        if not source_type:
            result.errors.append(f"media_sources[{source_id}]: missing type")
        elif str(source_type) not in SUPPORTED_MEDIA_SOURCE_TYPES:
            result.errors.append(f"media_sources[{source_id}]: unsupported type {source_type}")

        if source_type == "google_photos_shared_album" and not source.get("url"):
            result.errors.append(f"media_sources[{source_id}]: google_photos_shared_album requires url")

        if source_type == "local_folder" and not source.get("path"):
            result.errors.append(f"media_sources[{source_id}]: local_folder requires path")

    return source_ids


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

        for key in ("id", "date", "title", "route", "map"):
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


def _validate_day_media(data: dict[str, object], media_source_ids: set[str], result: ValidationResult) -> None:
    days = data.get("days")
    if not isinstance(days, list):
        return
    for day in days:
        if not isinstance(day, dict):
            continue
        day_id = str(day.get("id") or "<unknown>")
        media = day.get("media")
        if media is None:
            continue
        if not isinstance(media, dict):
            result.errors.append(f"{day_id}: media must be an object")
            continue
        source = media.get("source")
        if not source:
            result.errors.append(f"{day_id}: media.source is required")
        elif str(source) not in media_source_ids:
            result.errors.append(f"{day_id}: media.source references unknown media source {source}")

        filters = media.get("filters", {})
        if filters is not None and not isinstance(filters, dict):
            result.errors.append(f"{day_id}: media.filters must be an object")
