from __future__ import annotations

from datetime import datetime
from pathlib import Path


def captured_at_from_file(path: Path) -> str:
    timestamp = path.stat().st_mtime
    return datetime.fromtimestamp(timestamp).astimezone().isoformat(timespec="seconds")
