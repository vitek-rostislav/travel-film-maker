from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TimelineItem:
    id: str
    type: str
    start_seconds: int
    duration_seconds: int
    source_scene_id: str
    asset_id: str | None = None
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "start_seconds": self.start_seconds,
            "duration_seconds": self.duration_seconds,
            "source_scene_id": self.source_scene_id,
        }
        if self.asset_id:
            data["asset_id"] = self.asset_id
        if self.title:
            data["title"] = self.title
        if self.metadata:
            data["metadata"] = self.metadata
        return data


@dataclass(slots=True)
class NormalizedTimeline:
    fps: int
    aspect_ratio: str
    items: list[TimelineItem] = field(default_factory=list)

    def duration_seconds(self) -> int:
        if not self.items:
            return 0
        return max(item.start_seconds + item.duration_seconds for item in self.items)

    def to_dict(self) -> dict[str, Any]:
        return {
            "timeline": {
                "schema": "travel-film-maker.timeline.v1",
                "fps": self.fps,
                "aspect_ratio": self.aspect_ratio,
                "duration_seconds": self.duration_seconds(),
                "items": [item.to_dict() for item in self.items],
            }
        }
