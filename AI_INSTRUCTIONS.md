# AI Instructions

Use these rules when creating, editing, or refactoring Manim scenes in this repository.

The project is organized around one animation per file. Keep each file focused on a single concept and a single `Scene` class.

## Project Structure

- Put animation files under `animations/`.
- Keep one `Scene` class per animation file.
- Group related files into folders when that makes the project easier to browse.
- Keep support files such as shared palette helpers separate from scene files.

Example structure:

```text
animations/
  cpu/
    fetch_decode_execute_story.py
    while_loop_story.py
  math/
    floating_point_story.py
  palette.py
```

## Terminology Rules

These wording rules are strict.

### "New animation"

Interpret `new animation` as:

- Create a new Python file.
- Put it in `animations/` or the most appropriate subfolder.
- Add one `Scene` class inside that new file.

Examples:

- `Create a new animation about recursion` -> create a new file such as `animations/recursion/recursion_story.py`
- `I want a new animation called BinaryIntro` -> create a new file, not a new function inside an existing file

### "Add to my file"

Interpret `add to my file` as:

- Edit an existing file.
- Update the current `Scene` class, helper function, or supporting layout utility in that file.
- Do not create a new file unless the user explicitly asks for a new file.

Examples:

- `Add to my floating point file` -> update that existing file
- `Add another step to fetch_decode_execute_story.py` -> extend the existing scene or helpers in that file

### "New scene"

Interpret `new scene` from context:

- If the user also says `new animation`, create a new file.
- If the user says `add` or refers to an existing file, update that file instead of adding a second `Scene` class.
- If the request is ambiguous, prefer the file and wording the user explicitly named.

## File-Level Rules

At the top of every animation file, define exactly these two variables:

```python
RENDER_QUALITY = "medium"
COLOR_SCHEME = "Dark"
```

Add short comments describing:

- `low` = preview quality
- `medium` = standard render quality
- `high` = final render quality

That file's scene uses those settings.

## Visual Rules

- Keep scenes visually consistent across the repository.
- Prefer simple diagrams, labels, arrows, and clean motion.
- Make explanations visual-first and beginner-friendly.
- Prefer clarity over density.
- Avoid clutter, overlap, and off-screen clipping.
- Keep text short and readable.
- Remove objects that are no longer helping explain the idea.

## Palette Rules

- Use the shared palette helper instead of hardcoding one-off colors.
- Supported schemes are `Dark`, `Light`, and `Sepia`.
- Default to `Dark` unless the scene needs a different tone.
- Use semantic colors for background, surface, text, accent, border, and soft fills.

## Animation Structure

- Keep each explanation in a single focused `Scene` class.
- Use descriptive `Scene` class names.
- Keep helper functions in the same file when they improve clarity and reduce repetition.

## Running Animations

Run animation files directly:

```bash
python animations/fetch_decode_execute_story.py
python animations/toaster_black_box.py
```

Expected behavior:

- Running a file renders that file's single `Scene` class.
- The VS Code run/debug button for this workspace should target the current animation file directly.

## Validation Checklist

Before considering a scene complete, check that:

- the palette matches repository conventions
- no important objects overlap
- the scene progression is clear
- text is readable and not too dense
- old objects are removed when they stop helping
- the file still runs directly as a Python script

Do not run a full local render by default. If a visual check is needed, prefer a single-frame preview or the smallest useful render.

## Reference

Primary reference:

- https://docs.manim.community/en/stable/

Check the docs before using lesser-known classes, helpers, or render flags.
