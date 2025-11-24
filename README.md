# Manim Animation Projects

Collection of Manim animations featuring professional LaTeX rendering and GPU-accelerated shader effects.

## Projects

### 1. Binary to Text Animation (`binary_hello.py`)
Visualizes how binary data is read and decoded into text.

### 2. GPU Shader Demo (`gpu_shader_demo.py`)
Performance comparison between CPU and GPU rendering with shader effects.

### 3. GPU Compute Demo (`gpu_compute_demo.py`)
High-performance GPU compute demonstration optimized for AMD RX 9060XT with 2800+ objects.

## Description

### Binary to Text Animation
Shows how binary data is decoded:
- A line of binary data representing the word "Hello" (rendered with LaTeX)
- A read header that processes the binary data
- The binary moving from right to left through the read header
- Real-time binary-to-decimal conversion display
- Each byte being decoded and producing the output letters
- Professional typesetting using LaTeX throughout

### GPU Shader Demo
Demonstrates GPU vs CPU performance:
- Side-by-side visual comparison of CPU and GPU rendering
- Particle system with different complexities
- Real-time shader effects with animated color gradients
- Performance timing and speedup calculations
- Complex mesh rendering with 900+ synchronized elements

## Font Style Consistency

The animation uses a consistent font system:
- **MathTex**: For mathematical equations and symbols (conversions like `01001000₂ = 72₁₀`, checkmark)
- **Tex**: For LaTeX-formatted text (bold title with `\textbf{}`, monospace binary with `\texttt{}`)
- **Text**: For normal text labels and output (Read Header, Output label, decoded letters)

This ensures:
- Clean separation between math and text rendering
- Professional LaTeX typography for formatted elements
- Standard text rendering for labels and output

## Requirements

- Python 3.8+
- Manim Community Edition
- **LaTeX distribution** (TeX Live, MiKTeX, or TeXworks)
  - Required for rendering mathematical and text elements
  - Make sure `latex`, `dvisvgm`, and related tools are in your PATH
- **GPU**: AMD RX 9060XT 16GB (or similar)
- **GPU Drivers**: Mesa with RADV or AMDGPU-PRO
- **GPU Libraries**: ModernGL, PyOpenGL (installed via requirements.txt)

## Installation

Install Manim:
```bash
pip install manim
```

Or with requirements.txt:
```bash
pip install -r requirements.txt
```

**LaTeX Setup:**
- **Windows**: TeXworks, MiKTeX, or TeX Live
- **macOS**: MacTeX
- **Linux**: `sudo apt-get install texlive-full` (Debian/Ubuntu)

**GPU Setup for AMD RX 9060XT:**

**Windows (PowerShell):**
```powershell
# Run in PowerShell
.\setup_gpu.ps1
```

**Windows (Command Prompt):**
```cmd
setup_gpu.bat
```

**Linux/macOS:**
```bash
source setup_gpu.sh
```

The setup script will:
- Install GPU libraries (ModernGL, PyOpenGL)
- Configure environment variables for AMD GPU
- Enable hardware acceleration
- Install Manim with all dependencies

## Configuration

A `manim.cfg` file is included with optimized settings:
- **Cache disabled**: Prevents intermediate media/tex files from accumulating
- **Flush cache enabled**: Cleans up temporary files after rendering
- **60 fps**: Smooth animation playback
- **1080p resolution**: High quality output

## Usage

### Quick Start

**Step 1: Verify GPU setup**
```bash
python check_gpu.py
```

**Step 2: Configure AMD GPU environment**

**Windows PowerShell:**
```powershell
.\setup_gpu.ps1
```

**Windows Command Prompt:**
```cmd
setup_gpu.bat
```

**Linux/macOS:**
```bash
source setup_gpu.sh
```

**Binary to Text Animation:**
```bash
manim --renderer=opengl --write_to_movie -pqh binary_hello.py BinaryToText
```

**GPU Shader Demo:**
```bash
manim --renderer=opengl --write_to_movie -pqh gpu_shader_demo.py GPUShaderDemo
```

**GPU Compute Demo (2800+ objects - Maximum GPU Utilization):**
```bash
manim --renderer=opengl --write_to_movie -pqh gpu_compute_demo.py GPUComputeDemo
```

### GPU-Accelerated Rendering (Recommended)

For faster rendering with graphics card acceleration:

```bash
# High quality with GPU acceleration (FASTEST)
manim --renderer=opengl --write_to_movie -pqh binary_hello.py BinaryToText

# Low quality preview with GPU
manim --renderer=opengl --write_to_movie -pql binary_hello.py BinaryToText
```

### Standard Rendering (CPU)

```bash
# Render in high quality
manim -pqh binary_hello.py BinaryToText

# Render in low quality (faster preview)
manim -pql binary_hello.py BinaryToText

# Render in medium quality
manim -pqm binary_hello.py BinaryToText
```

### Clean Rendering (No Intermediate Files)

To ensure no tex/media files are left behind:

```bash
# The manim.cfg already has disable_caching=True and flush_cache=True
# But you can also explicitly clear cache before rendering:
manim --flush_cache -pqh binary_hello.py BinaryToText
```

**Note**:
- The `-p` flag automatically plays the video when rendering is complete
- Final output is saved in `media/videos/` directory
- With caching disabled, no intermediate files accumulate
- GPU rendering (OpenGL) is significantly faster than CPU rendering (Cairo)

## Output

The animation will:
1. Display a **bold LaTeX title** "Binary to Text Decoder"
2. Show a yellow **read header** box in the center
3. Display **binary representation** of "Hello" with letter annotations (H, e, l, l, o)
4. Move the binary from **right to left** through the read header
5. Flash the read header and current byte **red** when reading
6. Show **real-time conversion**: binary₂ = decimal₁₀ = "letter"
7. Display each decoded letter in the **output area** with monospace font
8. Add a **green checkmark** and final highlighted message
9. Professional **LaTeX rendering** throughout for crisp, publication-quality text

## Binary Encoding

The word "Hello" is encoded as:
- H = 01001000
- e = 01100101
- l = 01101100
- l = 01101100
- o = 01101111

---

## GPU Shader Demo Details

The `gpu_shader_demo.py` file demonstrates GPU acceleration advantages:

### Features:
- **Side-by-side comparison** of CPU vs GPU rendering
- **Particle system animation** (20 particles for CPU, 100+ for GPU)
- **Real-time shader effects** with color gradients
- **Performance metrics** showing speedup
- **Complex mesh rendering** (900+ dots with animated colors)

### Rendering Commands:

**GPU rendering (Recommended - Shows true performance):**
```bash
manim --renderer=opengl --write_to_movie -pqh gpu_shader_demo.py GPUShaderDemo
```

**CPU rendering (For comparison):**
```bash
manim -pqh gpu_shader_demo.py GPUShaderDemo
```

### What to Expect:
- GPU animation shows particles completing in **2 seconds**
- CPU animation shows particles completing in **6 seconds**
- Displays **3x speedup** with GPU
- Complex shader grid with 900+ animated dots demonstrates parallel processing
- Real-time color transformations showcase GPU shader capabilities

### Performance Benefits:
When using `--renderer=opengl`:
- **Parallel processing** of thousands of operations
- **Real-time shader effects** for complex color calculations
- **Faster frame rendering** for particle systems
- **Smooth animations** with higher particle counts

---

## GPU Compute Demo Details (AMD RX 9060XT Optimized)

The `gpu_compute_demo.py` file is specifically designed to maximize GPU utilization:

### What It Does:
This animation pushes your AMD RX 9060XT to its limits with:

1. **2000-Particle System** with real-time physics
   - Wave motion simulation
   - Complex vortex calculations
   - Explosion particle burst

2. **800-Point Fractal Pattern**
   - Golden angle spiral generation
   - Simultaneous color transformations
   - Rotation and scaling transforms

3. **Parallel GPU Operations**
   - All particles updated simultaneously
   - Color interpolation across 2800+ objects
   - Real-time position calculations

### Why This Uses Your GPU:

**With OpenGL Renderer (`--renderer=opengl`):**
- Each particle is a vertex processed by GPU
- Transformations happen on GPU shaders
- Color calculations run in parallel on GPU cores
- Your 16GB VRAM holds all object data
- AMD's RDNA architecture processes thousands of operations per frame

### Running for Maximum GPU Usage:

**Windows:**
```powershell
# 1. Setup AMD GPU environment
.\setup_gpu.ps1

# 2. Run with OpenGL renderer (GPU accelerated)
manim --renderer=opengl --write_to_movie -pqh gpu_compute_demo.py GPUComputeDemo

# 3. Monitor GPU usage while rendering:
# - Open Task Manager (Ctrl+Shift+Esc) -> Performance -> GPU
# - Use AMD Software: Adrenalin Edition for detailed metrics
# - Watch VRAM usage (should see several GB used)
# - GPU should hit 70-100% during particle animations
```

**Linux:**
```bash
# 1. Setup AMD GPU environment
source setup_gpu.sh

# 2. Run with OpenGL renderer (GPU accelerated)
manim --renderer=opengl --write_to_movie -pqh gpu_compute_demo.py GPUComputeDemo

# 3. Monitor GPU usage:
# Use 'radeontop' or 'nvtop' to see GPU utilization
watch -n 1 radeontop
```

### Expected Performance:
- **GPU Utilization**: 70-100% during particle effects
- **VRAM Usage**: 2-4 GB for object data
- **Frame Rate**: Smooth 60fps with OpenGL
- **Render Time**: ~1-2 minutes for full animation

### Optimization Tips:
1. Make sure AMD drivers are up to date
2. Use `source setup_gpu.sh` before rendering
3. Close other GPU-intensive applications
4. Use `-pqh` for full quality (tests GPU more)
5. Monitor with: `watch -n 1 radeontop` in another terminal

### Troubleshooting:

**Windows:**
If GPU usage is still low:
- Update AMD drivers to latest version from AMD.com
- Verify OpenGL renderer is active (check command output)
- Make sure you ran `.\setup_gpu.ps1` in the current PowerShell session
- Check Windows Display Settings -> Graphics Settings -> add Python as "High Performance"
- Ensure Python is using the dedicated AMD GPU (not integrated graphics)
- Use AMD Software: Adrenalin Edition to verify GPU is selected
- Try running PowerShell as Administrator

**Linux:**
If GPU usage is still low:
- Verify OpenGL renderer is active (check terminal output)
- Ensure AMD drivers support OpenGL 4.6+
- Run: `export MESA_GL_VERSION_OVERRIDE=4.6`
- Check: `glxinfo | grep "OpenGL renderer"` shows your AMD card
