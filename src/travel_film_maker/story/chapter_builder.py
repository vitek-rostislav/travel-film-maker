from __future__ import annotations

from collections import defaultdict
from typing import Any

from travel_film_maker.core.asset import Asset
from travel_film_maker.core.story import Chapter


def build_chapters(assets: list[Asset]) -> list[dict[str, object]]:
    by_date: dict[str, list[Asset]] = defaultdict(list)
    for asset in assets:
        date = asset.captured_at[:10] if asset.captured_at else "undated"
        by_date[date].append(asset)

    chapters: list[dict[str, object]] = []
    for index, date in enumerate(sorted(by_date), start=1):
        chapter = Chapter(
            id=f"day-{index:02d}",
            title=f"Day {index}",
            date=date,
            beats=[
                {"type": "chapter_card"},
                {"type": "map_route"},
                {"type": "establishing"},
                {"type": "road_sequence"},
                {"type": "evening_reflection"},
            ],
        )
        data = chapter.to_dict()
        data["asset_count"] = len(by_date[date])
        chapters.append(data)
    return chapters


def build_chapters_from_trip_plan(trip_plan: dict[str, Any], assets: list[Asset]) -> list[dict[str, object]]:
    asset_counts = _asset_counts_by_folder(assets)
    chapters: list[dict[str, object]] = []

    for day in trip_plan.get("days", []):
        beats = [{"type": "chapter_card"}]
        if day.get("map"):
            beats.append({"type": "map_route", **day["map"]})
        beats.extend({"type": "story_beat", "text": text} for text in day.get("story_beats", []))

        chapter: dict[str, object] = {
            "id": day["id"],
            "title": day["title"],
            "date": day["date"],
            "location": day.get("location"),
            "route": day.get("route"),
            "country_flags": day.get("country_flags", []),
            "stats": day.get("stats", {}),
            "mood": day.get("mood"),
            "beats": beats,
        }

        folder = day.get("assets", {}).get("folder") if isinstance(day.get("assets"), dict) else None
        if folder:
            chapter["assets"] = {"folder": folder}
            chapter["asset_count"] = asset_counts.get(folder.rstrip("/"), 0)
        chapters.append(chapter)

    return chapters


def trip_bounds_from_plan(trip_plan: dict[str, Any]) -> dict[str, object]:
    days = trip_plan.get("days", [])
    dates = [day["date"] for day in days if day.get("date")]
    trip: dict[str, object] = dict(trip_plan.get("trip", {}))
    if dates:
        trip["start"] = min(dates)
        trip["end"] = max(dates)
    return trip


def _asset_counts_by_folder(assets: list[Asset]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for asset in assets:
        parts = asset.path.split("/")
        for index in range(1, len(parts)):
            folder = "/".join(parts[:index])
            counts[folder] = counts.get(folder, 0) + 1
    return counts
