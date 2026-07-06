from __future__ import annotations

import argparse
import importlib.util
import shutil


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("doctor", help="Check local Travel Film Maker dependencies.")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> int:
    checks = [
        ("python-package", True, "travel-film-maker package is importable"),
        ("pyyaml", importlib.util.find_spec("yaml") is not None, "required for YAML project files"),
        ("ffprobe", shutil.which("ffprobe") is not None, "optional, needed for video metadata probing"),
        ("ffmpeg", shutil.which("ffmpeg") is not None, "optional, future preview/render support"),
    ]

    has_error = False
    for name, ok, note in checks:
        status = "ok" if ok else "missing"
        print(f"{status:7} {name:15} {note}")
        if name in {"pyyaml"} and not ok:
            has_error = True

    return 1 if has_error else 0
