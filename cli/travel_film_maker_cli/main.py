from __future__ import annotations

import argparse
from pathlib import Path

from travel_film_maker import __version__
from travel_film_maker_cli.commands.doctor import register as register_doctor
from travel_film_maker_cli.commands.init import register as register_init
from travel_film_maker_cli.commands.preview import register as register_preview
from travel_film_maker_cli.commands.render import register as register_render
from travel_film_maker_cli.commands.validate import register as register_validate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="travel-film-maker",
        description="Generate documentary travel film edit plans from media and GPS data.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    register_doctor(subparsers)
    register_validate(subparsers)
    register_preview(subparsers)
    register_render(subparsers)
    register_init(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
