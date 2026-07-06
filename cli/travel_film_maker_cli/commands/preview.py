from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.asset_engine.media_sources import summarize_media_sources
from travel_film_maker.asset_engine.scanner import scan_project_assets
from travel_film_maker.project_model.validation import validate_project_file
from travel_film_maker.story_engine.scenes import build_story_scenes
from travel_film_maker.style_engine.style import load_style_profile
from travel_film_maker.timeline_engine.builder import build_normalized_timeline


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("preview", help="Print an editor-agnostic project preview.")
    parser.add_argument("project", type=Path, nargs="?", default=Path.cwd(), help="Project directory or project.yaml path.")
    parser.add_argument("--show-scenes", action="store_true", help="Print scene-level details.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    result = validate_project_file(_project_file(args.project))
    if not result.ok or result.project is None:
        for warning in result.warnings:
            print(f"warning: {warning}")
        for error in result.errors:
            print(f"error: {error}")
        return 1

    project = result.project
    style = load_style_profile(project)
    media_sources = summarize_media_sources(project)
    assets = scan_project_assets(project)
    scenes = build_story_scenes(project, assets, style)
    timeline = build_normalized_timeline(project, scenes, style)

    print(f"Project: {project.title}")
    if project.subtitle:
        print(f"Subtitle: {project.subtitle}")
    print(f"Style: {style.name}")
    print(f"Route: {' -> '.join(project.route)}")
    print(f"Media sources: {len(media_sources)}")
    for source in media_sources:
        scope = "remote" if source.remote else "local"
        print(f"  - {source.id} ({source.type}, {scope}): {source.status}")
    print(f"Days: {len(project.days)}")
    print(f"Assets found: {len(assets)}")
    if any(source.remote for source in media_sources):
        print("Remote media is referenced only; no photos or videos are downloaded by preview.")
    print(f"Scenes: {len(scenes)}")
    print(f"Timeline items: {len(timeline.items)}")
    print(f"Estimated duration: {timeline.duration_seconds()}s")

    if args.show_scenes:
        print()
        for scene in scenes:
            print(f"{scene.id}: {scene.type} | {scene.title} | {scene.duration_hint_seconds}s")

    return 0


def _project_file(path: Path) -> Path:
    return path / "project.yaml" if path.is_dir() else path
