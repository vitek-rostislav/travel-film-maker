from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.core.project import default_project
from travel_film_maker.core.config import dump_yaml


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("init", help="Create a new Travel Film Maker project.")
    parser.add_argument("--title", default="Untitled Travel Film", help="Project title.")
    parser.add_argument("--id", default=None, help="Stable project id. Defaults to a slug from title.")
    parser.add_argument("--timezone", default="UTC", help="Project timezone.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    project_dir: Path = args.project_dir
    project_dir.mkdir(parents=True, exist_ok=True)

    for child in ("media/photos", "media/videos", "gps", "music", "exports"):
        (project_dir / child).mkdir(parents=True, exist_ok=True)

    project = default_project(title=args.title, project_id=args.id, timezone=args.timezone)
    dump_yaml(project_dir / "project.yaml", project)
    dump_yaml(project_dir / "assets.yaml", {"assets": []})
    dump_yaml(project_dir / "story.yaml", {"trip": {}, "chapters": []})
    dump_yaml(project_dir / "timeline.yaml", {"timeline": {"fps": 25, "tracks": {"video": [], "audio": []}}})

    print(f"Initialized Travel Film Maker project in {project_dir}")
    return 0
