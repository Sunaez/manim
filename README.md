# Binary to Text Animation

A Manim animation that visualizes how binary data is read and decoded into text.

## Description

This animation shows:
- A line of binary data representing the word "Hello"
- A read header that processes the binary data
- The binary moving from right to left through the read header
- Each byte being decoded and producing the output letters

## Requirements

- Python 3.8+
- Manim Community Edition

## Installation

```bash
pip install manim
```

Or with requirements.txt:
```bash
pip install -r requirements.txt
```

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
1. Display a title "Binary to Text Decoder"
2. Show a yellow read header in the center
3. Display binary representation of "Hello" starting from the right
4. Move the binary from right to left through the read header
5. Flash the read header red when reading each byte
6. Display each decoded letter in the output area
7. Highlight the final "Hello" output

## Binary Encoding

The word "Hello" is encoded as:
- H = 01001000
- e = 01100101
- l = 01101100
- l = 01101100
- o = 01101111
