#!/usr/bin/env python3
"""
Automatic GPU setup and launcher for ManimGL on Windows with AMD RX 9060XT.
This script automatically configures environment and runs manimgl with GPU acceleration.

Usage:
    python run_gpu.py gpu_compute_demo.py GPUComputeDemo
    python run_gpu.py binary_hello.py BinaryToText
"""

import os
import sys
import subprocess

def setup_gpu_environment():
    """Automatically configure GPU environment for VRAM usage."""

    # Force AMD GPU selection
    os.environ['MESA_GL_VERSION_OVERRIDE'] = '4.6'
    os.environ['FORCE_DISCRETE_GPU'] = '1'

    # AMD-specific VRAM settings
    os.environ['GPU_MAX_HEAP_SIZE'] = '100'
    os.environ['GPU_MAX_ALLOC_PERCENT'] = '100'
    os.environ['GPU_SINGLE_ALLOC_PERCENT'] = '100'

    # OpenGL settings
    os.environ['PYOPENGL_FULL_TRACE'] = '0'

    # Windows GPU preference
    os.environ['DXGI_ADAPTER'] = '0'  # Use first discrete GPU

    print("=" * 60)
    print("AMD RX 9060XT GPU Configuration for ManimGL")
    print("=" * 60)
    print(f"GPU_MAX_HEAP_SIZE: {os.environ['GPU_MAX_HEAP_SIZE']}")
    print(f"GPU_MAX_ALLOC_PERCENT: {os.environ['GPU_MAX_ALLOC_PERCENT']}")
    print(f"FORCE_DISCRETE_GPU: {os.environ['FORCE_DISCRETE_GPU']}")
    print("=" * 60)
    print()

def run_manim(args):
    """Run manimgl with GPU acceleration (OpenGL is default in ManimGL)."""

    # Build manimgl command - OpenGL is native, no flags needed!
    cmd = ['manimgl'] + args

    print("Running command:")
    print(" ".join(cmd))
    print()
    print("Monitor VRAM usage in Task Manager:")
    print("  Performance -> GPU -> Dedicated GPU Memory")
    print()
    print("ManimGL uses OpenGL by default - GPU acceleration is automatic!")
    print("=" * 60)
    print()

    # Run manimgl
    try:
        result = subprocess.run(cmd, check=True)
        print()
        print("=" * 60)
        print("Rendering complete!")
        print("=" * 60)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print(f"Error: ManimGL failed with exit code {e.returncode}")
        print("=" * 60)
        return e.returncode
    except FileNotFoundError:
        print()
        print("=" * 60)
        print("Error: 'manimgl' command not found!")
        print("Install ManimGL first: pip install manimgl")
        print("=" * 60)
        return 1

def main():
    """Main entry point."""

    if len(sys.argv) < 2:
        print("Usage: python run_gpu.py <script.py> <SceneName>")
        print()
        print("Examples:")
        print("  python run_gpu.py gpu_compute_demo.py GPUComputeDemo")
        print("  python run_gpu.py binary_hello.py BinaryToText")
        print()
        print("Note: ManimGL uses OpenGL natively - GPU acceleration is automatic!")
        print("      No quality flags needed - renders at optimal quality.")
        return 1

    # Setup GPU environment automatically
    setup_gpu_environment()

    # Run manim with provided arguments
    return run_manim(sys.argv[1:])

if __name__ == '__main__':
    sys.exit(main())
