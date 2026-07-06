from __future__ import annotations

from typing import Protocol


class Plugin(Protocol):
    name: str

    def register(self) -> None:
        """Register plugin hooks."""
