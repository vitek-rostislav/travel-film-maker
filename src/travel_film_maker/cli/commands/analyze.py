from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.analysis.quality_score import score_assets
from travel_film_maker.core.asset import Asset
from travel_film_maker.core.config import dump_yaml, load_yaml


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("analyze", help="Add initial technical scores to assets.yaml.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    project_dir: Path = args.project_dir
    data = load_yaml(project_dir / "assets.yaml")
    assets = [Asset.from_dict(item) for item in data.get("assets", [])]
    scored = score_assets(assets)
    dump_yaml(project_dir / "assets.yaml", {"assets": [asset.to_dict() for asset in scored]})
    print(f"Analyzed {len(scored)} assets")
    return 0
