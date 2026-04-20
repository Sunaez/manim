# Floating Point Story

This project contains a short educational Manim animation that explains floating-point numbers in a simple visual way.

The repository is organized so each animation lives in its own clearly named file inside `animations/`.

## Visual Theme

All videos in this project should use the shared palette helper with one of these scheme names:

- `Dark`
- `Light`
- `Sepia`

Default to `Dark` unless a scene intentionally needs a different tone.

- Keep text minimal and high-contrast
- Motion: smooth transitions, gentle zooms, and clear labels

## Animation Rules

- Keep each learning chunk isolated.
- Remove previous text, arrows, highlights, and helper shapes before introducing the next topic.
- Do not let old examples overlap with new examples unless the overlap is intentionally part of the explanation.

## Scene

The main scene is:

- `FloatingPointStory`

It shows four parts:

1. Introduction
2. Mantissa and exponent
3. Normalised vs unnormalised
4. Storage concept

## VS Code Run Button

The script reads its quality preset from the source file.
The default play button workflow should stay on the medium preset.

Available options:

- `low` = preview quality
- `medium` = standard render quality
- `high` = final render quality

## Running

From the terminal:

```powershell
python animations/floating_point_story.py
```

Or render directly with Manim:

```powershell
manim -pqm animations/floating_point_story.py FloatingPointStory
```

## Notes for Rendering

- Put `RENDER_QUALITY` and `COLOR_SCHEME` at the top of each animation file.
- Set `RENDER_QUALITY` to `medium` by default and add short comments near it explaining `low`, `medium`, and `high`.
- Prefer the shared palette helper for new scenes.
- Keep explanations beginner-friendly and visually driven.
