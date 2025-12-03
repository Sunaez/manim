# Manim Community Edition Demo

A comprehensive demonstration of Manim Community Edition features including text, shapes, transformations, mathematical expressions, and graphs.

## Requirements

- Python 3.8 or higher
- Windows operating system
- **Latest version** of Manim Community Edition (automatically installed)

## Setup

### 1. Install Python

Download and install Python from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation

### 2. Set Up Virtual Environment

Run once to create the isolated environment:

```powershell
.\setup_venv.bat
```

This installs the **latest version** of Manim CE in a virtual environment.

## Usage

### Step 1: Activate Virtual Environment

Every time you open a new terminal, activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

You'll see `(venv)` appear in your prompt.

### Step 2: Render Animations

Use manim commands directly:

```powershell
# Medium quality, 30fps (recommended - meets 30fps minimum)
manim -pqm manim_demo.py ManimFeatureDemo

# High quality, 60fps
manim -pqh manim_demo.py ManimFeatureDemo

# 4K quality, 60fps
manim -pqk manim_demo.py ManimFeatureDemo
```

**Note**: Don't use `-pql` (low quality) as it only renders at 15fps, below the 30fps minimum requirement.

### Quality Options

| Flag | Resolution | FPS | Preview | Use Case |
|------|------------|-----|---------|----------|
| `-pqm` | 720p | 30 | ✓ | **Recommended** - Minimum quality |
| `-pqh` | 1080p | 60 | ✓ | High quality output |
| `-pqk` | 2160p | 60 | ✓ | 4K production quality |
| `-ql` | 480p | 15 | ✗ | ❌ Below 30fps minimum |

**Flags explained:**
- `-p` = Preview video after rendering
- `-q` = Quality preset (l/m/h/k)

### Step 3: Deactivate (Optional)

When done:

```powershell
deactivate
```

## Output Location

Videos are automatically saved to `media/videos/` with this structure:

```
media/videos/manim_demo/
├── 720p30/ManimFeatureDemo.mp4    # Medium quality (-pqm)
├── 1080p60/ManimFeatureDemo.mp4   # High quality (-pqh)
└── 2160p60/ManimFeatureDemo.mp4   # 4K quality (-pqk)
```

**Temporary files are automatically cleaned** - only the final video remains.

To manually remove all output:

```powershell
Remove-Item -Recurse -Force media
```

## Updating to Latest Manim Version

To update to the newest version of Manim CE:

**Option 1: Recreate environment (recommended)**
```powershell
.\setup_venv.bat
# Choose "y" when prompted to recreate
```

**Option 2: Upgrade manually**
```powershell
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

When working with this Manim project, follow these rules:

### Core Requirements

1. **30fps minimum** - Always use `-pqm`, `-pqh`, or `-pqk` (never `-pql`)
2. **Video output only** - No images, no GIFs, only `.mp4` files in `media/videos/`
3. **Latest Manim CE** - Always use the virtual environment with latest version
4. **No temporary files** - Manim automatically cleans up, don't create extra files
5. **Windows PowerShell** - All commands for Windows environment

### Workflow

**Before rendering (first time only):**
```powershell
.\setup_venv.bat  # Sets up venv with latest Manim CE
```

**Every rendering session:**
```powershell
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Render with manim directly
manim -pqm script.py SceneName   # 30fps minimum
manim -pqh script.py SceneName   # 60fps high quality
manim -pqk script.py SceneName   # 60fps 4K quality
```

### Allowed Commands

✅ **DO use:**
- `manim -pqm` (720p, 30fps) - **Minimum acceptable**
- `manim -pqh` (1080p, 60fps)
- `manim -pqk` (2160p, 60fps)

❌ **DON'T use:**
- `manim -pql` (Only 15fps - below minimum)
- `manim -s` (Still images, not video)
- `manim --format=gif` (GIF format, not video)
- Any command without activating venv first

### Output Structure

Videos save to: `media/videos/[script_name]/[quality]/[SceneName].mp4`

Example:
```
media/videos/manim_demo/720p30/ManimFeatureDemo.mp4
```

Temporary files are auto-cleaned. Only final video remains.

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
1. Ensure virtual environment is activated (`.\venv\Scripts\Activate.ps1`)
2. Check LaTeX is installed for `MathTex()` usage
3. Verify all imports are from `manim` package
4. Ensure Python 3.8+ is being used
5. Check that scene class name matches command

**For faster development iterations:**
- Use `-qm` (30fps, 720p) for quick previews - still meets minimum requirements
- Use `-qh` or `-qk` for final production output
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
