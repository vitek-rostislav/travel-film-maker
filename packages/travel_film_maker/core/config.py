from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:
    yaml = None  # type: ignore[assignment]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        content = handle.read()
    if yaml is not None:
        return yaml.safe_load(content) or {}
    try:
        return json.loads(content) if content.strip() else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Install PyYAML to read non-JSON YAML files: {path}") from exc


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        if yaml is not None:
            yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)
        else:
            json.dump(data, handle, indent=2)
            handle.write("\n")


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
