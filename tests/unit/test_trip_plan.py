from travel_film_maker.core.asset import Asset
from travel_film_maker.core.trip_plan import is_trip_plan
from travel_film_maker.story.chapter_builder import build_chapters_from_trip_plan, trip_bounds_from_plan


def test_trip_plan_builds_story_chapters():
    trip_plan = {
        "project": {"title": "Roadtrip"},
        "trip": {"totals": {"drive_km": 100}},
        "days": [
            {
                "id": "day01",
                "date": "2026-06-27",
                "title": "Start",
                "location": "Vienna",
                "route": "Ostrava -> Vienna",
                "country_flags": ["CZ", "AT"],
                "stats": {"drive_km": 277},
                "story_beats": ["Leaving home"],
                "assets": {"folder": "assets/day01"},
                "map": {"type": "google-earth", "from": "Ostrava", "to": "Vienna"},
                "mood": "departure",
            }
        ],
    }
    assets = [Asset(id="img_0001", type="photo", path="assets/day01/IMG_0001.jpg")]

    assert is_trip_plan(trip_plan)
    assert trip_bounds_from_plan(trip_plan)["start"] == "2026-06-27"

    chapters = build_chapters_from_trip_plan(trip_plan, assets)

    assert chapters[0]["id"] == "day01"
    assert chapters[0]["asset_count"] == 1
    assert chapters[0]["beats"][1]["type"] == "google-earth"
