from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker import __version__
from travel_film_maker.cli.commands.analyze import register as register_analyze
from travel_film_maker.cli.commands.export import register as register_export
from travel_film_maker.cli.commands.ingest import register as register_ingest
from travel_film_maker.cli.commands.init import register as register_init
from travel_film_maker.cli.commands.plan import register as register_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="travel-film-maker",
        description="Generate documentary travel film edit plans from media and GPS data.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project directory containing project.yaml and generated data files.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    register_init(subparsers)
    register_ingest(subparsers)
    register_analyze(subparsers)
    register_plan(subparsers)
    register_export(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
