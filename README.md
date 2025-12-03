# Manim Community Edition Demo

A comprehensive demonstration of Manim Community Edition features including text, shapes, transformations, mathematical expressions, and graphs.

## Requirements

- Python 3.8 or higher
- Windows operating system
- **Latest version** of Manim Community Edition (automatically installed)

## Quick Start (Recommended)

### 1. Install Python

Download and install Python from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation

### 2. Set Up Virtual Environment

Double-click `setup_venv.bat` or run in PowerShell:

```bash
.\setup_venv.bat
```

This will:
- ✅ Create an isolated Python virtual environment in `venv/`
- ✅ Install the **latest version** of Manim CE automatically
- ✅ Install all dependencies
- ✅ Verify the installation

**This only needs to be run once!** (or when you want to update to the latest Manim version)

### 3. Run the Demo

**In PowerShell:**
```bash
.\run_manim.bat manim_demo.py ManimFeatureDemo -pqm
```

**Or double-click** `run_manim.bat` and it will prompt you for the script and scene names.

That's it! The animation will render and open automatically.

## Running Animations

### Using the Run Script (Recommended)

The `run_manim.bat` script automatically uses the virtual environment.

**In PowerShell (note the `.\` prefix):**
```bash
# Medium quality, 30fps (recommended)
.\run_manim.bat manim_demo.py ManimFeatureDemo -pqm

# High quality, 60fps
.\run_manim.bat manim_demo.py ManimFeatureDemo -pqh

# Low quality for quick tests
.\run_manim.bat manim_demo.py ManimFeatureDemo -pql
```

**In Command Prompt (CMD):**
```cmd
# No .\ prefix needed in CMD
run_manim.bat manim_demo.py ManimFeatureDemo -pqm
```

**Or just double-click** `run_manim.bat` (it will show usage help)

### Command Options

- `-p` : Preview the video after rendering
- `-q` : Quality level
  - `-ql` : Low quality (480p, 15fps) - Fast rendering
  - `-qm` : Medium quality (720p, 30fps) - **Recommended minimum**
  - `-qh` : High quality (1080p, 60fps)
  - `-qk` : 4K quality (2160p, 60fps)

### Manual Method (Advanced)

If you prefer to activate the environment manually:

```bash
# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Run manim directly
manim -pqm manim_demo.py ManimFeatureDemo

# Deactivate when done
deactivate
```

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

## Updating to Latest Manim Version

This project is configured to always use the **latest version** of Manim CE.

To update to the newest version:

1. Run the setup script again:
   ```bash
   .\setup_venv.bat
   ```

2. When prompted "Do you want to recreate it?", type `y` and press Enter

3. The script will:
   - Remove the old virtual environment
   - Create a fresh environment
   - Install the latest Manim CE version
   - Verify the installation

**Or manually update:**
```bash
.\venv\Scripts\Activate.ps1
pip install --upgrade manim
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

1. **Always use the virtual environment** - Use `run_manim.bat` script or activate `venv/` manually
2. **Always render at 30fps minimum** - Use `-qm` (medium quality, 30fps) or higher
3. **Video output only** - Only produce video files in the `media/videos/` directory
4. **No temporary files** - Manim handles cleanup automatically; never create additional temp files
5. **Use Manim Community Edition** - Not ManimGL or other variants (always latest version)
6. **Windows-only environment** - All commands should be Windows-compatible

### Environment Setup

**First time setup:**
```bash
.\setup_venv.bat  # Creates venv and installs latest Manim CE
```

**To update to latest Manim version:**
```bash
.\setup_venv.bat  # Choose "yes" to recreate environment
```

### Rendering Commands

**DO use (with virtual environment in PowerShell):**
```bash
.\run_manim.bat manim_demo.py ManimFeatureDemo -pqm  # Medium quality, 30fps
.\run_manim.bat manim_demo.py ManimFeatureDemo -pqh  # High quality, 60fps
```

**OR manually activate venv:**
```bash
.\venv\Scripts\Activate.ps1
manim -pqm manim_demo.py ManimFeatureDemo
```

**DON'T use:**
```bash
manim -pql ...  # Only 15fps, below minimum requirement
manim -s ...    # Still images, not video
manim --format=gif ...  # GIF format, not video
pip install manim  # Don't install globally, use venv!
run_manim.bat ...  # Missing .\ prefix in PowerShell
```

**Note**: PowerShell requires `.\` prefix for scripts in the current directory. CMD does not.

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
