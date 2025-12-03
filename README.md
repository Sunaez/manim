# Manim Community Edition Demo

A comprehensive demonstration of Manim Community Edition features including text, shapes, transformations, mathematical expressions, and graphs.

## Requirements

- Python 3.8 or higher
- Manim Community Edition 0.18.0 or higher
- Windows operating system

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/)

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
manim --version
```

## Running the Animation

To render the demo animation as a video file in the `media/videos` folder:

```bash
manim -pql manim_demo.py ManimFeatureDemo
```

### Command Options

- `-p` : Preview the video after rendering
- `-q` : Quality level
  - `-ql` : Low quality (480p, 15fps) - Fast rendering
  - `-qm` : Medium quality (720p, 30fps) - **Recommended**
  - `-qh` : High quality (1080p, 60fps)
  - `-qk` : 4K quality (2160p, 60fps)

### Recommended Command for 30fps Output

```bash
manim -pqm manim_demo.py ManimFeatureDemo
```

This renders at 720p resolution with 30fps and automatically opens the video when complete.

## Output Location

All video files are saved to:
```
media/videos/manim_demo/720p30/ManimFeatureDemo.mp4
```

The path changes based on quality settings:
- Low quality: `480p15/`
- Medium quality: `720p30/`
- High quality: `1080p60/`

## Cleaning Temporary Files

Manim automatically cleans up temporary files during rendering. The only output is the final video file in the `media/videos` directory.

To manually clean all generated files:
```bash
rm -rf media/
```

Or on Windows:
```cmd
rmdir /s /q media
```

## Features Demonstrated

The demo showcases:

1. **Text & Typography** - Various text styles, colors, and gradients
2. **Shapes & Colors** - Circles, squares, triangles with fills and animations
3. **Transformations** - Shape morphing and scaling
4. **Mathematical Expressions** - LaTeX equations and formulas
5. **Graphs & Functions** - Plotting sine and cosine functions
6. **Complex Animations** - Combined effects and layered scenes

## Animation Structure

The main scene `ManimFeatureDemo` contains multiple sub-scenes:
- `intro_scene()` - Title and introduction
- `text_scene()` - Text demonstrations
- `shapes_scene()` - Shape creation and manipulation
- `transformation_scene()` - Morphing animations
- `math_scene()` - Mathematical equations
- `graph_scene()` - Function plotting
- `finale_scene()` - Closing sequence

---

## Instructions for AI Assistants / Chatbots

When working with this Manim project, follow these guidelines:

### General Principles

1. **Always render at 30fps minimum** - Use `-qm` (medium quality, 30fps) or higher
2. **Video output only** - Only produce video files in the `media/videos/` directory
3. **No temporary files** - Manim handles cleanup automatically; never create additional temp files
4. **Use Manim Community Edition** - Not ManimGL or other variants
5. **Windows-only environment** - All commands should be Windows-compatible

### Rendering Commands

**DO use:**
```bash
manim -pqm manim_demo.py ManimFeatureDemo  # Medium quality, 30fps
manim -pqh manim_demo.py ManimFeatureDemo  # High quality, 60fps
```

**DON'T use:**
```bash
manim -pql ...  # Only 15fps, below minimum requirement
manim -s ...    # Still images, not video
manim --format=gif ...  # GIF format, not video
```

### File Management

- **Output directory**: `media/videos/[filename]/[quality]/[SceneName].mp4`
- **Temporary files**: Automatically managed by Manim, no manual intervention needed
- **Partial renders**: Not allowed - always render complete scenes
- **Cache**: Manim uses `.media_cache/` but cleans it automatically

### Code Guidelines

1. **Scene Configuration**:
   - Always set `config.frame_rate = 30` or higher at the top of files
   - Use `Scene` class from `manim` package
   - Import: `from manim import *`

2. **Text Rendering**:
   - Use `Text()` for regular text
   - Use `MathTex()` for mathematical equations (LaTeX)
   - Never use `Tex()` for non-mathematical text

3. **Animation Quality**:
   - Minimum 30fps frame rate
   - Use smooth transitions with appropriate `run_time` values
   - Add `self.wait()` between scenes for pacing

4. **Best Practices**:
   - Clear scenes between major sections with `self.clear()`
   - Use descriptive scene names
   - Comment complex animations
   - Organize code into methods for readability

### Common Tasks

**Adding a new scene:**
```python
def new_scene(self):
    """Description of what this scene does"""
    header = Text("Scene Title", font_size=48, color=BLUE)
    self.play(Write(header))
    # ... scene content ...
    self.play(FadeOut(header))
```

**Modifying animations:**
- Keep `run_time` values reasonable (0.5-2 seconds typically)
- Use `self.wait()` for pauses
- Chain animations with `AnimationGroup` or `LaggedStart`

**Testing changes:**
```bash
manim -pqm manim_demo.py ManimFeatureDemo
```

### Troubleshooting

**If rendering fails:**
1. Check LaTeX is installed for `MathTex()` usage
2. Verify all imports are from `manim` package
3. Ensure Python 3.8+ is being used
4. Check that scene class name matches command

**Performance issues:**
- Use `-ql` for quick previews during development
- Use `-qm` or `-qh` for final output
- Avoid creating thousands of objects in a single scene

### Output Verification

After rendering, verify:
- ✓ Video file exists in `media/videos/` directory
- ✓ Frame rate is 30fps or higher (check with media player)
- ✓ No temporary files remain in working directory
- ✓ Video plays smoothly without artifacts

---

## Additional Resources

- [Manim Community Edition Documentation](https://docs.manim.community/)
- [Example Gallery](https://docs.manim.community/en/stable/examples.html)
- [Discord Community](https://discord.gg/manim)

## License

This demo project is provided as-is for educational purposes.
