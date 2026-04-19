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

- Use a dark blue background in every scene.
- Keep a consistent dark-mode palette unless a scene has a strong, intentional reason to vary it.
- Avoid bright white backgrounds.
- Avoid clashing neon colors.
- Keep text minimal, readable, and high-contrast.

### Dark Mode Palette

- Background: `#0f172a`
- Surface: `#1e293b`
- Primary blue: `#3b82f6`
- Teal: `#14b8a6`
- Green: `#22c55e`
- Orange: `#f59e0b`
- Red: `#ef4444`
- Gold: `#eab308`
- Text: `#f8fafc`
- Muted text: `#cbd5e1`

## Layout And Readability

- Make sure nothing important overlaps.
- Check spacing between titles, labels, arrows, formulas, and diagrams before considering a scene finished.
- Make sure objects do not clip off-screen unless that is intentional.
- Keep compositions balanced and leave enough empty space for the viewer to follow the main idea.
- Keep text short enough to read comfortably during playback.
- Prefer fewer labels with stronger hierarchy over many small labels competing for attention.
- Use local renders or local previews to catch overlap and spacing issues early because they are faster than waiting for a full final render.

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

- `low` = 480p, 30fps preview
- `medium` = 1280x720, 30fps
- `high` = 1920x1080, 60fps

When adding new scenes or instructions, preserve these presets and keep the run button workflow compatible with them.

At the top of every animation file, define exactly these two variables:

- `FRAME_RATE` for the scene frame rate
- `RENDER_QUALITY` for the chosen render preset

Default to:

- `FRAME_RATE = 30`
- `RENDER_QUALITY = "medium"`

Add short source comments explaining:

- `low` = 480p, 30fps preview
- `medium` = 1280x720, 30fps
- `high` = 1920x1080, 60fps

## Implementation Rules

- Set `config.frame_rate` from the top-level `FRAME_RATE` variable.
- Use the top-level `RENDER_QUALITY` variable inside `render_scene()` so the preset can be changed directly in the file.
- Keep each animation in its own clearly named file inside `animations/`.
- Keep scene names stable when possible so VS Code launch configurations remain valid.
- Keep helper methods inside the scene file when they improve readability and reduce repetition.
- Reuse palette constants instead of hardcoding many one-off colors throughout a scene.
- Keep render helpers consistent with the existing repository pattern.
- The default VS Code play button should continue to render the medium preset at 720p and 30fps.

## Validation Checklist

Before considering a scene complete, check that:

- the background and palette match the repository style
- no important objects overlap
- continuity is used when the concept is evolving, and old content is removed when it stops helping
- text is readable and not too dense
- arrows and labels point clearly to the intended objects
- the scene works at the medium preset without layout problems
- the file still follows the repository render helper pattern

## Reference

Use the Manim Community documentation as the primary reference when writing or editing scenes:

- https://docs.manim.community/en/stable/

Check the docs before using lesser-known classes, animation helpers, or render flags so the code stays accurate and idiomatic.
