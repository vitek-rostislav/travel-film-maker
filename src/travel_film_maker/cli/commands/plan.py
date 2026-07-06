from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.core.asset import Asset
from travel_film_maker.core.config import dump_yaml, load_yaml
from travel_film_maker.core.project import default_project
from travel_film_maker.core.trip_plan import load_trip_plan, timeline_output_path
from travel_film_maker.edit.selector import build_timeline
from travel_film_maker.story.chapter_builder import build_chapters, build_chapters_from_trip_plan, trip_bounds_from_plan


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("plan", help="Create story.yaml and an editable timeline from assets.")
    parser.add_argument("--fps", type=int, default=None, help="Override timeline FPS.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    project_dir: Path = args.project_dir
    trip_plan = load_trip_plan(project_dir)
    project = _load_project(project_dir, trip_plan)
    assets_data = load_yaml(project_dir / "assets.yaml") if (project_dir / "assets.yaml").exists() else {"assets": []}
    assets = [Asset.from_dict(item) for item in assets_data.get("assets", [])]

    if trip_plan:
        chapters = build_chapters_from_trip_plan(trip_plan, assets)
        trip = trip_bounds_from_plan(trip_plan)
    else:
        chapters = build_chapters(assets)
        trip = _trip_bounds(assets)

    fps = args.fps or int(project.get("output", {}).get("fps", 25))
    timeline = build_timeline(assets, fps=fps)
    output_path = timeline_output_path(project_dir)

    dump_yaml(project_dir / "story.yaml", {"trip": trip, "chapters": chapters})
    dump_yaml(output_path, {"timeline": timeline.to_dict()})
    print(f"Planned {len(chapters)} chapters and {timeline.clip_count()} clips into {output_path}")
    return 0


def _trip_bounds(assets: list[Asset]) -> dict[str, str]:
    dates = sorted(asset.captured_at[:10] for asset in assets if asset.captured_at)
    if not dates:
        return {}
    return {"start": dates[0], "end": dates[-1]}


def _load_project(project_dir: Path, trip_plan: dict[str, object] | None) -> dict[str, object]:
    project_path = project_dir / "project.yaml"
    if project_path.exists():
        return load_yaml(project_path)

    trip_project = trip_plan.get("project", {}) if trip_plan else {}
    title = str(trip_project.get("title", "Untitled Travel Film"))
    project = default_project(title=title, timezone="Europe/Prague")
    project["project"]["language"] = trip_project.get("language", "cs")
    project["project"]["style"] = trip_project.get("style", "long-way-round-inspired")
    if trip_project.get("aspect_ratio"):
        project["output"]["aspect_ratio"] = trip_project["aspect_ratio"]
    return project
