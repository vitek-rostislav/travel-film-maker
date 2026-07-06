from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.core.asset import Asset
from travel_film_maker.core.config import dump_yaml, load_yaml
from travel_film_maker.edit.selector import build_timeline
from travel_film_maker.story.chapter_builder import build_chapters


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("plan", help="Create story.yaml and timeline.yaml from assets.")
    parser.add_argument("--fps", type=int, default=None, help="Override timeline FPS.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    project_dir: Path = args.project_dir
    project = load_yaml(project_dir / "project.yaml")
    assets_data = load_yaml(project_dir / "assets.yaml")
    assets = [Asset.from_dict(item) for item in assets_data.get("assets", [])]

    chapters = build_chapters(assets)
    fps = args.fps or int(project.get("output", {}).get("fps", 25))
    timeline = build_timeline(assets, fps=fps)

    dump_yaml(project_dir / "story.yaml", {"trip": _trip_bounds(assets), "chapters": chapters})
    dump_yaml(project_dir / "timeline.yaml", {"timeline": timeline.to_dict()})
    print(f"Planned {len(chapters)} chapters and {timeline.clip_count()} clips")
    return 0


def _trip_bounds(assets: list[Asset]) -> dict[str, str]:
    dates = sorted(asset.captured_at[:10] for asset in assets if asset.captured_at)
    if not dates:
        return {}
    return {"start": dates[0], "end": dates[-1]}
