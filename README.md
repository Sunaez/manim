# Manim Educational Animations

This repository is set up for focused Manim animations grouped by concept.

## Structure

- One file should contain one `Scene` class.
- One folder can contain multiple related animation files.
- Use folders to group topics such as `cpu/`, `math/`, or `systems/`.

Example:

```text
animations/
  cpu/
    fetch_decode_execute_story.py
    while_loop_story.py
  math/
    floating_point_story.py
  palette.py
```

## Core Workflow

Run animation files directly.

```bash
python animations/fetch_decode_execute_story.py
python animations/toaster_black_box.py
```

## VS Code

- `Ctrl+Shift+B` opens tasks for running the current animation file.
- The Run/Debug button is configured to call the current file directly.

## Naming Rules

- `new animation` means create a new file
- `add to my file` means edit an existing file and update its current scene or helpers
- keep one animation per file

## File Template

Each animation file should define:

```python
RENDER_QUALITY = "medium"
# low: preview quality
# medium: standard render quality
# high: final render quality

COLOR_SCHEME = "Dark"
```

That file's animation uses those settings.

## More Detail

- [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md)
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
