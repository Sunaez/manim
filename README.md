# Binary to Text Animation

A Manim animation that visualizes how binary data is read and decoded into text, featuring professional LaTeX rendering.

## Description

This animation shows:
- A line of binary data representing the word "Hello" (rendered with LaTeX)
- A read header that processes the binary data
- The binary moving from right to left through the read header
- Real-time binary-to-decimal conversion display
- Each byte being decoded and producing the output letters
- Professional typesetting using LaTeX throughout

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

## Usage

To render the animation:

```bash
# Render in high quality
manim -pqh binary_hello.py BinaryToText

# Render in low quality (faster preview)
manim -pql binary_hello.py BinaryToText

# Render in medium quality
manim -pqm binary_hello.py BinaryToText
```

**Note**: Manim renders the complete animation as a single video file. The `-p` flag automatically plays the video when rendering is complete. Output will be saved in the `media/videos/` directory.

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
