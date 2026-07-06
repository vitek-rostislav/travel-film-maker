from __future__ import annotations

from collections import defaultdict

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
