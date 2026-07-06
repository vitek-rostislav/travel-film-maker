# DaVinci Resolve Export

Travel Film Maker exports DaVinci Resolve timelines through two layers:

1. FCPXML for the core editable timeline.
2. Resolve Python scripting for bins, metadata, markers, project setup, and later Fusion templates.

The internal timeline model should remain editor-neutral. DaVinci Resolve is an export backend, not the canonical data model.
