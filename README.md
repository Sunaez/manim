# Floating Point Story

This project contains a short educational Manim animation that explains floating-point numbers in a simple visual way.

The repository is organized so each animation lives in its own clearly named file inside `animations/`.

## Visual Theme

All videos in this project should use a dark blue theme:

- Background: `#0f172a`
- Surface blocks: `#1e293b`
- Accents: blue `#3b82f6`, teal `#14b8a6`, green `#22c55e`, orange `#f59e0b`, red `#ef4444`, gold `#eab308`
- Text: keep it minimal and high-contrast
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
The default play button workflow should stay on the medium preset: 720p at 30fps.

Available options:

- `low` = 480p, 30fps preview
- `medium` = 1280x720, 30fps
- `high` = 1080p, 60fps

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

- Put `FRAME_RATE` and `RENDER_QUALITY` at the top of each animation file.
- Set `config.frame_rate` from `FRAME_RATE`.
- Set `RENDER_QUALITY` to `medium` by default and add short comments near it explaining `low`, `medium`, and `high`.
- Prefer the dark blue visual language for new scenes.
- Keep explanations beginner-friendly and visually driven.
