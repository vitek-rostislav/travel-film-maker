from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.core.config import dump_json, load_yaml
from travel_film_maker.export.davinci.fcpxml import export_fcpxml
from travel_film_maker.export.opentimelineio import export_otio_json


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("export", help="Export the edit plan for a target editor.")
    parser.add_argument("--format", choices=["fcpxml", "otio-json"], default="fcpxml")
    parser.add_argument("--output", type=Path, default=None, help="Output file path.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    project_dir: Path = args.project_dir
    project = load_yaml(project_dir / "project.yaml")
    assets = load_yaml(project_dir / "assets.yaml")
    timeline = load_yaml(project_dir / "timeline.yaml")
    export_dir = project_dir / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    if args.format == "fcpxml":
        output = args.output or export_dir / "timeline.fcpxml"
        export_fcpxml(output, project, assets, timeline)
    else:
        output = args.output or export_dir / "timeline.otio.json"
        dump_json(output, export_otio_json(project, assets, timeline))

    print(f"Exported {args.format} to {output}")
    return 0
