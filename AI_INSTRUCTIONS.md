# AI Instructions

Use these rules when creating, editing, or refactoring Manim scenes in this repository.

The goal is consistent, readable, dark-mode educational animations that render cleanly and stay compatible with the existing VS Code workflow.

## Core Goals

- Keep scenes visually consistent across the repository.
- Make explanations visual-first, simple, and beginner-friendly.
- Prefer clarity over density.
- Avoid layout issues, overlap, and clutter.
- Keep rendering workflow and scene structure predictable.

## Theme

- Every animation must support a single `COLOR_SCHEME` name with one of: `Dark`, `Light`, `Sepia`.
- Default to `Dark` unless the scene needs a different tone.
- Use the shared palette mapping rather than hardcoding one-off colors in the scene body.
- Avoid clashing neon colors.
- Keep text minimal, readable, and high-contrast.

### Shared Palette Rule

- Keep palette values in a shared helper so every animation can switch schemes by name.
- The supported scheme names are `Dark`, `Light`, and `Sepia`.
- Use scheme-specific semantic roles such as background, surface, text, border, accent, and soft fill.

## Layout And Readability

- Make sure nothing important overlaps.
- Before rendering, run a preflight layout check on positioned mobjects whenever practical.
- Prefer failing fast in code with explicit overlap checks or assertions for labels, formulas, callouts, axes, and panels that must not intersect.
- Use bounding-box checks for a fast first pass, and use tighter geometric checks only when the scene needs them.
- Check spacing between titles, labels, arrows, formulas, and diagrams before considering a scene finished.
- Make sure objects do not clip off-screen unless that is intentional.
- Keep compositions balanced and leave enough empty space for the viewer to follow the main idea.
- Keep text short enough to read comfortably during playback.
- Prefer fewer labels with stronger hierarchy over many small labels competing for attention.
- Do not run a full local render by default.
- If you need a visual sanity check, use at most a single-frame render or equivalent static preview to catch overlap and spacing issues.

## Animation Style

- Prefer simple shapes, arrows, labels, and clean geometric layouts.
- Use smooth transitions and gentle motion.
- Keep explanations visual-first and beginner-friendly.
- Avoid heavy jargon unless the scene is explicitly about technical detail.
- Animate the idea itself when possible, not just labels around it.
- Use emphasis effects sparingly so they remain meaningful.
- Avoid overloading a frame with too many simultaneous callouts.

## Scene Structure

- Teach in clear chunks.
- Keep continuity when the concept is evolving.
- Clear previously shown objects when they no longer help explain the current idea.
- Do not accidentally leave old labels, highlights, or guide objects visible when they no longer support the current idea.
- If an earlier object remains on screen, it must have a clear purpose in the next beat of the animation.
- Keep scene progression easy to follow from top to bottom and left to right where possible.

## Text And Math

- Prefer `Text()` for regular prose.
- Prefer `MathTex()` for formulas, expressions, and symbolic notation.
- Keep prose concise.
- Use readable font sizes and maintain a consistent text scale across a file.
- Avoid large blocks of explanatory text when a diagram or transformation can show the same idea.

## Quality Presets

Every animation file should support these quality options:

- `low` = preview quality
- `medium` = standard render quality
- `high` = final render quality

When adding new scenes or instructions, preserve these presets and keep the run button workflow compatible with them.

At the top of every animation file, define exactly these two variables:

- `RENDER_QUALITY` for the chosen render preset
- `COLOR_SCHEME` for the palette name

Default to:

- `RENDER_QUALITY = "medium"`
- `COLOR_SCHEME = "Dark"`

Add short source comments explaining:

- `low` = preview quality
- `medium` = standard render quality
- `high` = final render quality

## Implementation Rules

- When asked to create something new, create a new Python file for it.
- If the concept is different, do not add it to an existing file; put it in a separate new Python file instead.
- Use the top-level `RENDER_QUALITY` variable inside `render_scene()` so the preset can be changed directly in the file.
- Use the top-level `COLOR_SCHEME` variable to select the shared palette helper.
- Keep each animation in its own clearly named file inside `animations/`.
- Keep scene names stable when possible so VS Code launch configurations remain valid.
- Keep helper methods inside the scene file when they improve readability and reduce repetition.
- Reuse palette constants through the shared palette helper instead of hardcoding many one-off colors throughout a scene.
- Keep render helpers consistent with the existing repository pattern.
- The default VS Code play button should continue to render the medium preset as the standard render quality.
- When the VS Code play button starts a render, the launch workflow should automatically open the completed animation file after rendering finishes.

## Validation Checklist

Before considering a scene complete, check that:

- the background and palette match the repository style
- no important objects overlap
- continuity is used when the concept is evolving, and old content is removed when it stops helping
- text is readable and not too dense
- arrows and labels point clearly to the intended objects
- if a visual check is needed, use only a single-frame preview rather than a full animation render
- the file still follows the repository render helper pattern

## Reference

Use the Manim Community documentation as the primary reference when writing or editing scenes:

- https://docs.manim.community/en/stable/

Check the docs before using lesser-known classes, animation helpers, or render flags so the code stays accurate and idiomatic.
