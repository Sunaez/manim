@echo off
REM Windows GPU Setup Script for AMD RX 9060XT
REM Run this with: setup_gpu.bat

echo === AMD RX 9060XT GPU Setup for ManimGL (Windows) ===
echo.

REM Set AMD GPU environment variables for Windows
set MESA_GL_VERSION_OVERRIDE=4.6
set FORCE_DISCRETE_GPU=1

REM AMD-specific settings for VRAM usage
set GPU_MAX_HEAP_SIZE=100
set GPU_MAX_ALLOC_PERCENT=100
set GPU_SINGLE_ALLOC_PERCENT=100

REM Disable fallback to CPU
set PYOPENGL_FULL_TRACE=0

echo Installing required Python packages...
echo.

REM Install packages with specific versions for Windows
pip install --upgrade pip
pip install manimgl moderngl PyOpenGL PyOpenGL-accelerate numpy pillow

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === Installation Complete ===
    echo.
    echo Environment variables set for GPU VRAM usage:
    echo   MESA_GL_VERSION_OVERRIDE = %MESA_GL_VERSION_OVERRIDE%
    echo   FORCE_DISCRETE_GPU = %FORCE_DISCRETE_GPU%
    echo   GPU_MAX_HEAP_SIZE = %GPU_MAX_HEAP_SIZE%
    echo   GPU_MAX_ALLOC_PERCENT = %GPU_MAX_ALLOC_PERCENT%
    echo.
    echo === ManimGL Setup Complete ===
    echo.
    echo ManimGL uses OpenGL natively - GPU acceleration is automatic!
    echo.
    echo Next Steps:
    echo   1. Close AMD Software: Adrenalin Edition if running
    echo   2. Make sure no other apps are using GPU
    echo   3. Run: python check_gpu.py
    echo   4. Run: python run_gpu.py gpu_compute_demo.py GPUComputeDemo
    echo.
    echo Monitor VRAM usage in Task Manager -^> Performance -^> GPU -^> Dedicated GPU Memory
    echo.
) else (
    echo.
    echo === Installation Failed ===
    echo.
    echo Try installing manually:
    echo   pip install manim moderngl PyOpenGL PyOpenGL-accelerate numpy
)

echo.
echo IMPORTANT: These environment variables are set for this Command Prompt session only.
echo To use them, keep this window open and run manim from here.
echo.

pause
