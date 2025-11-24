# Manim Animation Projects

Collection of Manim animations featuring professional LaTeX rendering and GPU-accelerated shader effects.

## Projects

### 1. Binary to Text Animation (`binary_hello.py`)
Visualizes how binary data is read and decoded into text.

### 2. GPU Shader Demo (`gpu_shader_demo.py`)
Performance comparison between CPU and GPU rendering with shader effects.

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

## Configuration

A `manim.cfg` file is included with optimized settings:
- **Cache disabled**: Prevents intermediate media/tex files from accumulating
- **Flush cache enabled**: Cleans up temporary files after rendering
- **60 fps**: Smooth animation playback
- **1080p resolution**: High quality output

## Usage

### Quick Start

**Binary to Text Animation:**
```bash
manim --renderer=opengl --write_to_movie -pqh binary_hello.py BinaryToText
```

**GPU Shader Demo:**
```bash
manim --renderer=opengl --write_to_movie -pqh gpu_shader_demo.py GPUShaderDemo
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
