from __future__ import annotations

from pathlib import Path
from typing import Any

from travel_film_maker.core.asset import Asset, asset_id_from_path
from travel_film_maker.ingest.exif import captured_at_from_file

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv"}


def ingest_project_media(project_dir: Path, project: dict[str, Any]) -> list[Asset]:
    source_entries = project.get("sources", {}).get("media", [])
    source_paths = [(project_dir / entry["path"]).resolve() for entry in source_entries if "path" in entry]
    assets: list[Asset] = []

    for source_path in source_paths:
        if not source_path.exists():
            continue
        for path in sorted(source_path.rglob("*")):
            if not path.is_file():
                continue
            asset_type = _asset_type(path)
            if not asset_type:
                continue
            assets.append(
                Asset(
                    id=_dedupe_id(asset_id_from_path(path), assets),
                    type=asset_type,
                    path=str(path.relative_to(project_dir)),
                    captured_at=captured_at_from_file(path),
                    tags=_default_tags(asset_type),
                )
            )

    return sorted(assets, key=lambda asset: (asset.captured_at or "", asset.path))


def _asset_type(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix in PHOTO_EXTENSIONS:
        return "photo"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    return None


def _dedupe_id(candidate: str, assets: list[Asset]) -> str:
    existing = {asset.id for asset in assets}
    if candidate not in existing:
        return candidate
    index = 2
    while f"{candidate}_{index}" in existing:
        index += 1
    return f"{candidate}_{index}"


def _default_tags(asset_type: str) -> list[str]:
    return ["still"] if asset_type == "photo" else ["movement"]
