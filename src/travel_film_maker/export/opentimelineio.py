from __future__ import annotations

from typing import Any


def export_otio_json(project: dict[str, Any], assets: dict[str, Any], timeline: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "travel-film-maker.otio-json.v1",
        "project": project.get("project", {}),
        "assets": assets.get("assets", []),
        "timeline": timeline.get("timeline", {}),
    }
