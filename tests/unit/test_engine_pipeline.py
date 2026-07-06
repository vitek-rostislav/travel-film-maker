from travel_film_maker.asset_engine.scanner import scan_project_assets
from travel_film_maker.core.config import dump_yaml
from travel_film_maker.project_model.model import load_project_model
from travel_film_maker.story_engine.scenes import build_story_scenes
from travel_film_maker.style_engine.style import load_style_profile
from travel_film_maker.timeline_engine.builder import build_normalized_timeline


def test_external_project_builds_editor_agnostic_timeline(tmp_path):
    project_dir = tmp_path / "Europe2026"
    (project_dir / "assets" / "day01").mkdir(parents=True)
    dump_yaml(project_dir / "project.yaml", _project_yaml())
    dump_yaml(project_dir / "style.yaml", _style_yaml())

    project = load_project_model(project_dir / "project.yaml")
    style = load_style_profile(project)
    assets = scan_project_assets(project)
    scenes = build_story_scenes(project, assets, style)
    timeline = build_normalized_timeline(project, scenes, style)

    assert project.title == "Europe 2026"
    assert len(project.days) == 1
    assert len(assets) == 0
    assert len(scenes) == 3
    assert timeline.items[0].type == "chapter_card"
    assert timeline.to_dict()["timeline"]["schema"] == "travel-film-maker.timeline.v1"


def _project_yaml():
    return {
        "project": {
            "title": "Europe 2026",
            "style": "long-way-round",
            "language": "en",
            "aspect_ratio": "16:9",
        },
        "trip": {
            "totals": {"drive_km": 100},
            "route": ["Ostrava", "Vienna"],
        },
        "days": [
            {
                "id": "day01",
                "date": "2026-06-27",
                "title": "Leaving Home",
                "location": "Vienna",
                "route": "Ostrava -> Vienna",
                "country_flags": ["CZ", "AT"],
                "stats": {"drive_km": 100},
                "highlights": ["Packing the car"],
                "assets": {"folder": "assets/day01"},
                "map": {"type": "google-earth", "from": "Ostrava", "to": "Vienna"},
                "mood": "departure",
            }
        ],
    }


def _style_yaml():
    return {
        "style": {
            "name": "long-way-round",
            "pacing": {"photo_seconds": 5, "video_seconds": 6, "map_seconds": 7, "chapter_seconds": 4},
        }
    }
