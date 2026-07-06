from pathlib import Path

from travel_film_maker.asset_engine.media_sources import summarize_media_sources
from travel_film_maker.core.config import dump_yaml
from travel_film_maker.project_model.model import load_project_model
from travel_film_maker.project_model.validation import validate_project_file


def test_google_photos_shared_album_is_valid_remote_source(tmp_path):
    project_file = tmp_path / "project.yaml"
    dump_yaml(project_file, _project())

    result = validate_project_file(project_file)
    project = load_project_model(project_file)

    assert result.ok
    assert project.media_sources[0].id == "google_photos_main"
    assert project.media_sources[0].type == "google_photos_shared_album"
    assert project.days[0].media.source == "google_photos_main"

    summaries = summarize_media_sources(project)
    assert summaries[0].remote
    assert "download not implemented" in summaries[0].status


def test_day_media_source_must_exist(tmp_path):
    project_file = tmp_path / "project.yaml"
    project = _project()
    project["days"][0]["media"]["source"] = "missing"
    dump_yaml(project_file, project)

    result = validate_project_file(project_file)

    assert not result.ok
    assert "unknown media source missing" in result.errors[0]


def _project():
    return {
        "project": {
            "title": "Europe 2026",
            "style": "long-way-round",
            "language": "en",
            "aspect_ratio": "16:9",
        },
        "trip": {"route": ["Ostrava", "Vienna"]},
        "media_sources": [
            {
                "id": "google_photos_main",
                "type": "google_photos_shared_album",
                "url": "https://photos.app.goo.gl/example",
                "mapping": {"default_day_strategy": "exif_date", "fallback_day_strategy": "manual"},
            }
        ],
        "days": [
            {
                "id": "day01",
                "date": "2026-06-27",
                "title": "Ostrava -> Vienna",
                "location": "Vienna",
                "route": "Ostrava -> Vienna",
                "highlights": ["Departure"],
                "media": {"source": "google_photos_main", "filters": {"date": "2026-06-27"}},
                "map": {"type": "route"},
                "mood": "departure",
            }
        ],
    }
