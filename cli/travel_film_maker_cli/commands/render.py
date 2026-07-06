from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.asset_engine.scanner import scan_project_assets
from travel_film_maker.core.config import dump_json
from travel_film_maker.project_model.validation import validate_project_file
from travel_film_maker.story_engine.scenes import build_story_scenes
from travel_film_maker.style_engine.style import load_style_profile
from travel_film_maker.timeline_engine.builder import build_normalized_timeline


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("render", help="Build the normalized timeline for a project. Video rendering is not implemented yet.")
    parser.add_argument("project", type=Path, help="Project directory or project.yaml path.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    project_file = args.project / "project.yaml" if args.project.is_dir() else args.project
    result = validate_project_file(project_file)
    if not result.ok or result.project is None:
        for warning in result.warnings:
            print(f"warning: {warning}")
        for error in result.errors:
            print(f"error: {error}")
        return 1

    project = result.project
    style = load_style_profile(project)
    assets = scan_project_assets(project)
    scenes = build_story_scenes(project, assets, style)
    timeline = build_normalized_timeline(project, scenes, style)
    output_path = project.root_dir / "output" / "timeline.normalized.json"
    dump_json(output_path, timeline.to_dict())

    print(f"Built normalized timeline: {output_path}")
    print("Video rendering is not implemented yet.")
    return 0
