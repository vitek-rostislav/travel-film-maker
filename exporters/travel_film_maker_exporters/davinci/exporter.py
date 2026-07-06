from __future__ import annotations

from pathlib import Path

from travel_film_maker.core.config import dump_json
from travel_film_maker.timeline_engine.model import NormalizedTimeline


class DavinciResolveExporter:
    name = "davinci-resolve"

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def export(self, timeline: NormalizedTimeline) -> None:
        # Initial exporter skeleton: write the normalized model for inspection.
        # FCPXML/Resolve scripting can consume the same model later.
        dump_json(self.output_path, timeline.to_dict())
