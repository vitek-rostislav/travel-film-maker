# DaVinci Resolve Export

Travel Film Maker exports DaVinci Resolve timelines as one backend fed by the normalized timeline model.

DaVinci Resolve must not be the internal architecture. The export path should remain:

1. Project Model, Style Engine, Asset Engine and Story Engine produce scenes.
2. Timeline Engine converts scenes into a normalized timeline.
3. DaVinci exporter translates that normalized timeline to FCPXML and/or Resolve scripting.

Future exporters should consume the same normalized timeline model.
