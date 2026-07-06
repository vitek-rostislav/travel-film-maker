from __future__ import annotations

from pathlib import Path
from datetime import datetime

from travel_film_maker.core.asset import Asset, asset_id_from_path
from travel_film_maker.project_model.model import ProjectModel

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv"}


def scan_project_assets(project: ProjectModel) -> list[Asset]:
    assets: list[Asset] = []
    for day in project.days:
        folder = project.root_dir / day.asset_folder
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*")):
            if not path.is_file():
                continue
            asset_type = detect_asset_type(path)
            if not asset_type:
                continue
            tags = ["day:" + day.id, "highlight-source"]
            assets.append(
                Asset(
                    id=_dedupe_id(asset_id_from_path(path), assets),
                    type=asset_type,
                    path=str(path.relative_to(project.root_dir)),
                    captured_at=captured_at_from_file(path),
                    tags=tags,
                )
            )
    return sorted(assets, key=lambda asset: (asset.captured_at or "", asset.path))


def detect_asset_type(path: Path) -> str | None:
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


def captured_at_from_file(path: Path) -> str:
    timestamp = path.stat().st_mtime
    return datetime.fromtimestamp(timestamp).astimezone().isoformat(timespec="seconds")
