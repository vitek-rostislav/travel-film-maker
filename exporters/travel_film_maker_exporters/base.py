from __future__ import annotations

from typing import Protocol

from travel_film_maker.timeline_engine.model import NormalizedTimeline


class TimelineExporter(Protocol):
    name: str

    def export(self, timeline: NormalizedTimeline) -> None:
        """Export a normalized timeline to a target tool."""
