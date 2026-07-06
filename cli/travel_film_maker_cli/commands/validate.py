from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker.project_model.validation import validate_project_file


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("validate", help="Validate a Travel Film Maker project YAML.")
    parser.add_argument("project", type=Path, nargs="?", default=Path.cwd(), help="Project directory or project.yaml path.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    result = validate_project_file(_project_file(args.project))
    if result.project:
        print(f"Project: {result.project.title}")
        print(f"Days: {len(result.project.days)}")
        print(f"Route: {' -> '.join(result.project.route)}")

    for warning in result.warnings:
        print(f"warning: {warning}")
    for error in result.errors:
        print(f"error: {error}")

    print("valid" if result.ok else "invalid")
    return 0 if result.ok else 1


def _project_file(path: Path) -> Path:
    return path / "project.yaml" if path.is_dir() else path
