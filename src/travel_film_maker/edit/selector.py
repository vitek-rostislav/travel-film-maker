from __future__ import annotations

from travel_film_maker.core.asset import Asset
from travel_film_maker.core.timeline import Timeline, TimelineClip
from travel_film_maker.edit.ken_burns import default_ken_burns
from travel_film_maker.edit.pacing import default_clip_duration


def build_timeline(assets: list[Asset], fps: int) -> Timeline:
    selected = sorted(assets, key=lambda asset: _asset_sort_key(asset))[:120]
    video_clips: list[TimelineClip] = []
    current_frame = 0

    for asset in selected:
        duration = default_clip_duration(asset.type)
        video_clips.append(
            TimelineClip(
                asset_id=asset.id,
                start=_frames_to_timecode(current_frame, fps),
                duration=duration,
                effect=default_ken_burns() if asset.type == "photo" else None,
            )
        )
        current_frame += _timecode_to_frames(duration, fps)

    return Timeline(fps=fps, video_clips=video_clips)


def _asset_sort_key(asset: Asset) -> tuple[float, str, str]:
    rating = float(asset.technical.get("rating", 0.0))
    return (-rating, asset.captured_at or "", asset.path)


def _frames_to_timecode(frames: int, fps: int) -> str:
    total_seconds, frame = divmod(frames, fps)
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frame:02d}"


def _timecode_to_frames(timecode: str, fps: int) -> int:
    hours, minutes, seconds, frames = (int(part) for part in timecode.split(":"))
    return (((hours * 60) + minutes) * 60 + seconds) * fps + frames
