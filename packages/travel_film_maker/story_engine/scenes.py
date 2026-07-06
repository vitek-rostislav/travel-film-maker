from __future__ import annotations

from dataclasses import dataclass, field

from travel_film_maker.core.asset import Asset
from travel_film_maker.project_model.model import Day, ProjectModel
from travel_film_maker.style_engine.style import StyleProfile


@dataclass(slots=True)
class Scene:
    id: str
    day_id: str
    type: str
    title: str
    intent: str
    duration_hint_seconds: int
    assets: list[Asset] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)


def build_story_scenes(project: ProjectModel, assets: list[Asset], style: StyleProfile) -> list[Scene]:
    assets_by_day = _assets_by_day(assets)
    scenes: list[Scene] = []
    for day in project.days:
        day_assets = assets_by_day.get(day.id, [])
        scenes.extend(_scenes_for_day(day, day_assets, style))
    return scenes


def _scenes_for_day(day: Day, assets: list[Asset], style: StyleProfile) -> list[Scene]:
    scenes = [
        Scene(
            id=f"{day.id}-chapter",
            day_id=day.id,
            type="chapter_card",
            title=day.title,
            intent="Introduce day, location, route and travel statistics.",
            duration_hint_seconds=style.pacing["chapter_seconds"],
            metadata={
                "date": day.date,
                "location": day.location,
                "route": day.route.label,
                "statistics": day.statistics,
                "country_flags": day.country_flags,
            },
        )
    ]

    if day.route.map:
        scenes.append(
            Scene(
                id=f"{day.id}-map",
                day_id=day.id,
                type="map",
                title=day.route.label,
                intent="Show geographic progression before the day sequence.",
                duration_hint_seconds=style.pacing["map_seconds"],
                metadata=day.route.map,
            )
        )

    for index, highlight in enumerate(day.highlights, start=1):
        scenes.append(
            Scene(
                id=f"{day.id}-highlight-{index:02d}",
                day_id=day.id,
                type="highlight",
                title=highlight,
                intent=_documentary_intent(index, day),
                duration_hint_seconds=_highlight_duration(assets, style),
                assets=assets,
                metadata={"mood": day.mood, "location": day.location},
            )
        )
    return scenes


def _assets_by_day(assets: list[Asset]) -> dict[str, list[Asset]]:
    result: dict[str, list[Asset]] = {}
    for asset in assets:
        day_tags = [tag.removeprefix("day:") for tag in asset.tags if tag.startswith("day:")]
        for day_id in day_tags:
            result.setdefault(day_id, []).append(asset)
    return result


def _highlight_duration(assets: list[Asset], style: StyleProfile) -> int:
    if any(asset.type == "video" for asset in assets):
        return style.pacing["video_seconds"]
    return style.pacing["photo_seconds"]


def _documentary_intent(index: int, day: Day) -> str:
    if index == 1:
        return f"Establish the day narrative in {day.location}."
    return "Develop the travel sequence with place, movement and family observations."
