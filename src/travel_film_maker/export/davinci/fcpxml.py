from __future__ import annotations

from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element, ElementTree, SubElement


def export_fcpxml(path: Path, project: dict[str, Any], assets: dict[str, Any], timeline: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fps = int(timeline.get("timeline", {}).get("fps", 25))
    project_title = project.get("project", {}).get("title", "Travel Film")
    timeline_name = project.get("output", {}).get("davinci", {}).get("timeline_name", f"{project_title} - Assembly")

    root = Element("fcpxml", version="1.10")
    resources = SubElement(root, "resources")
    format_id = "r1"
    SubElement(resources, "format", id=format_id, name=f"FFVideoFormat{fps}p", frameDuration=f"1/{fps}s")

    asset_map = {asset["id"]: asset for asset in assets.get("assets", [])}
    for index, asset in enumerate(assets.get("assets", []), start=2):
        asset["fcpxml_ref"] = f"r{index}"
        SubElement(
            resources,
            "asset",
            id=asset["fcpxml_ref"],
            name=asset["id"],
            src=Path(asset["path"]).as_posix(),
        )

    library = SubElement(root, "library")
    event = SubElement(library, "event", name=project_title)
    project_node = SubElement(event, "project", name=timeline_name)
    sequence = SubElement(project_node, "sequence", format=format_id, tcStart="0s", tcFormat="NDF")
    spine = SubElement(sequence, "spine")

    clips = timeline.get("timeline", {}).get("tracks", {}).get("video", [{}])[0].get("clips", [])
    for clip in clips:
        asset_id = clip.get("asset_id")
        asset = asset_map.get(asset_id)
        if not asset:
            continue
        SubElement(
            spine,
            "asset-clip",
            name=asset_id,
            ref=asset["fcpxml_ref"],
            offset=_timecode_to_seconds(clip["start"], fps),
            duration=_timecode_to_seconds(clip["duration"], fps),
        )

    ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def _timecode_to_seconds(timecode: str, fps: int) -> str:
    hours, minutes, seconds, frames = (int(part) for part in timecode.split(":"))
    total = (hours * 3600) + (minutes * 60) + seconds
    numerator = (total * fps) + frames
    return f"{numerator}/{fps}s"
