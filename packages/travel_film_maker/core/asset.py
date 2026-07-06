from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Asset:
    id: str
    type: str
    path: str
    captured_at: str | None = None
    duration: float | None = None
    location: dict[str, Any] | None = None
    technical: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Asset":
        return cls(
            id=str(data["id"]),
            type=str(data["type"]),
            path=str(data["path"]),
            captured_at=data.get("captured_at"),
            duration=data.get("duration"),
            location=data.get("location"),
            technical=dict(data.get("technical") or {}),
            tags=list(data.get("tags") or []),
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "path": self.path,
        }
        if self.captured_at:
            data["captured_at"] = self.captured_at
        if self.duration is not None:
            data["duration"] = self.duration
        if self.location:
            data["location"] = self.location
        if self.technical:
            data["technical"] = self.technical
        if self.tags:
            data["tags"] = self.tags
        return data


def asset_id_from_path(path: Path) -> str:
    stem = path.stem.lower().replace(" ", "_")
    return "".join(char for char in stem if char.isalnum() or char in {"_", "-"})
