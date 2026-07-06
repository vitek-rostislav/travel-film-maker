# Style Engine

The default style is a road-trip documentary inspired by long-form travel series.

## Visual Tone

- Documentary pacing over social-media speed.
- Real geography and route progression should stay visible.
- Photos use restrained Ken Burns movement.
- Videos should carry motion, place atmosphere, and road rhythm.

## Structure

- Open with a route or departure cue.
- Build each day around movement, place, friction, and reflection.
- Use chapter cards sparingly.
- Keep generated map shots functional and legible.

## Style Profile Responsibilities

The Style Engine reads `style.yaml` from the external travel project and defines:

- chapter card layout
- map style
- typography
- transitions
- pacing
- Ken Burns behavior
- subtitle placement and tone

## Export Boundary

Style decisions are applied before exporter-specific translation. DaVinci Resolve, Premiere, CapCut and FFmpeg exporters should consume the same normalized timeline data.
