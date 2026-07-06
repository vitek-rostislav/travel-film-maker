from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.core.config import dump_yaml, load_yaml
from travel_film_maker.ingest.filesystem import ingest_project_media


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("ingest", help="Scan configured media sources into assets.yaml.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    project_dir: Path = args.project_dir
    project = load_yaml(project_dir / "project.yaml")
    assets = ingest_project_media(project_dir, project)
    dump_yaml(project_dir / "assets.yaml", {"assets": [asset.to_dict() for asset in assets]})
    print(f"Ingested {len(assets)} assets into {project_dir / 'assets.yaml'}")
    return 0
