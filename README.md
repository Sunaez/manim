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

## LaTeX Features

The animation uses LaTeX for enhanced visual quality:
- **Bold title** with `\textbf{}`
- **Monospace binary** with `\texttt{}`
- **Small caps** for labels with `\textsc{}`
- **Mathematical notation** for base conversions (binary₂ = decimal₁₀)
- **Checkmark symbol** for completion
- **Professional typography** throughout

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
