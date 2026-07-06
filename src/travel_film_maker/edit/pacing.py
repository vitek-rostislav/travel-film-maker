from __future__ import annotations


def default_clip_duration(asset_type: str) -> str:
    if asset_type == "video":
        return "00:00:06:00"
    return "00:00:05:00"
