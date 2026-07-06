from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TimelineClip:
    asset_id: str | None
    start: str
    duration: str
    type: str | None = None
    effect: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "start": self.start,
            "duration": self.duration,
        }
        if self.asset_id:
            data["asset_id"] = self.asset_id
        if self.type:
            data["type"] = self.type
        if self.effect:
            data["effect"] = self.effect
        return data


@dataclass(slots=True)
class Timeline:
    fps: int
    video_clips: list[TimelineClip] = field(default_factory=list)
    audio_clips: list[TimelineClip] = field(default_factory=list)

    def clip_count(self) -> int:
        return len(self.video_clips) + len(self.audio_clips)

    def to_dict(self) -> dict[str, Any]:
        return {
            "fps": self.fps,
            "tracks": {
                "video": [
                    {
                        "id": "v1",
                        "clips": [clip.to_dict() for clip in self.video_clips],
                    }
                ],
                "audio": [
                    {
                        "id": "a1",
                        "clips": [clip.to_dict() for clip in self.audio_clips],
                    }
                ],
            },
        }
