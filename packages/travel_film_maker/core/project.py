from __future__ import annotations

import re
from typing import Any


def default_project(title: str, project_id: str | None = None, timezone: str = "UTC") -> dict[str, Any]:
    stable_id = project_id or slugify(title)
    return {
        "version": 1,
        "project": {
            "id": stable_id,
            "title": title,
            "timezone": timezone,
            "language": "en",
            "style": "long-way-round-inspired",
        },
        "sources": {
            "media": [{"path": "./media/photos"}, {"path": "./media/videos"}],
            "gps": [{"path": "./gps"}],
        },
        "output": {
            "fps": 25,
            "resolution": "3840x2160",
            "aspect_ratio": "16:9",
            "davinci": {
                "export_mode": "fcpxml",
                "timeline_name": f"{title} - Assembly",
            },
        },
        "style": {
            "pacing": "documentary",
            "photo_motion": "ken_burns",
            "chapter_cards": True,
            "map_transitions": True,
            "voiceover": True,
        },
    }


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "travel-film"
