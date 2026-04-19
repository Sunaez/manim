# AI Instructions

Use these rules when editing or adding Manim videos in this repository.

## Theme

- Keep every video on a dark blue background.
- Use a fixed dark-mode palette for consistency across scenes.
- Avoid bright white backgrounds and avoid clashing neon colors.
- Keep text minimal and readable.

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

## Animation Style

- Prefer simple shapes, arrows, and labels.
- Use smooth transitions and gentle zooms.
- Keep explanations visual-first and beginner-friendly.
- Avoid heavy jargon unless the scene is explicitly about technical detail.
- When teaching in chunks, fully clear the previous chunk before introducing the next one.
- Do not leave earlier objects, labels, or highlights visible when the animation moves to a new concept.

## Quality Presets

The main script supports these quality options:

- `low` = 480p, 30fps preview
- `medium` = 1280x720, 30fps
- `high` = 1080p, 60fps

When adding new scenes or instructions, preserve these presets and keep the run button workflow compatible with them.

## Implementation Rules

- Use `config.frame_rate = 30` or higher.
- Keep the dark blue theme in every scene.
- Apply the same dark-mode palette across new scenes unless a scene has a strong reason to vary it.
- Prefer `Text()` for regular prose and `MathTex()` for formulas.
- Keep the scene names stable so VS Code launch configs remain valid.
- Keep the repository organized so each animation lives in its own clearly named file inside `animations/`.
- The default VS Code play button should render the medium preset at 720p and 30fps.
- Use the Manim Community documentation as the primary reference when writing or editing scenes:
  - https://docs.manim.community/en/stable/
- Check the docs before using lesser-known classes, animation helpers, or render flags so the code stays accurate and idiomatic.
