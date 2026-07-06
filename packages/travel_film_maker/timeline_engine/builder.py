from __future__ import annotations

from travel_film_maker.project_model.model import ProjectModel
from travel_film_maker.story_engine.scenes import Scene
from travel_film_maker.style_engine.style import StyleProfile
from travel_film_maker.timeline_engine.model import NormalizedTimeline, TimelineItem


def build_normalized_timeline(
    project: ProjectModel,
    scenes: list[Scene],
    style: StyleProfile,
    fps: int = 25,
) -> NormalizedTimeline:
    timeline = NormalizedTimeline(fps=fps, aspect_ratio=project.aspect_ratio)
    cursor = 0

    for scene in scenes:
        item = _item_from_scene(scene, cursor, style)
        timeline.items.append(item)
        cursor += item.duration_seconds

    return timeline


def _item_from_scene(scene: Scene, start_seconds: int, style: StyleProfile) -> TimelineItem:
    metadata = dict(scene.metadata)
    if scene.type == "highlight" and scene.assets:
        asset = scene.assets[0]
        metadata["camera_movement"] = style.ken_burns if asset.type == "photo" else {"type": "locked"}
        metadata["transition"] = style.transitions["default"]
        return TimelineItem(
            id=f"tl-{scene.id}",
            type="asset",
            start_seconds=start_seconds,
            duration_seconds=scene.duration_hint_seconds,
            source_scene_id=scene.id,
            asset_id=asset.id,
            title=scene.title,
            metadata=metadata,
        )

    metadata["transition"] = style.transitions["chapter"] if scene.type == "chapter_card" else style.transitions["default"]
    return TimelineItem(
        id=f"tl-{scene.id}",
        type=scene.type,
        start_seconds=start_seconds,
        duration_seconds=scene.duration_hint_seconds,
        source_scene_id=scene.id,
        title=scene.title,
        metadata=metadata,
    )
