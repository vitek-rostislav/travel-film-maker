from __future__ import annotations

from dataclasses import dataclass

from travel_film_maker.project_model.model import ProjectModel


@dataclass(slots=True)
class MediaSourceSummary:
    id: str
    type: str
    remote: bool
    status: str


REMOTE_SOURCE_TYPES = {
    "google_photos_shared_album",
    "google_drive",
    "icloud_export",
    "dropbox",
    "onedrive",
}


def summarize_media_sources(project: ProjectModel) -> list[MediaSourceSummary]:
    summaries: list[MediaSourceSummary] = []
    for source in project.media_sources:
        remote = source.type in REMOTE_SOURCE_TYPES
        status = "remote metadata only; download not implemented" if remote else "local scan supported"
        summaries.append(MediaSourceSummary(id=source.id, type=source.type, remote=remote, status=status))
    return summaries
