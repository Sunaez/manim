@echo off
REM Windows GPU Setup Script for AMD RX 9060XT
REM Run this with: setup_gpu.bat

echo === GPU Setup for Manim with AMD RX 9060XT (Windows) ===
echo.

REM Set AMD GPU environment variables for Windows
set MESA_GL_VERSION_OVERRIDE=4.6
set FORCE_DISCRETE_GPU=1

echo Installing required Python packages...
echo.

REM Install packages
pip install manim moderngl PyOpenGL PyOpenGL-accelerate numpy

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === Installation Complete ===
    echo.
    echo Environment variables set:
    echo   MESA_GL_VERSION_OVERRIDE = %MESA_GL_VERSION_OVERRIDE%
    echo   FORCE_DISCRETE_GPU = %FORCE_DISCRETE_GPU%
    echo.
    echo === GPU Setup Complete ===
    echo.
    echo Usage:
    echo   manim --renderer=opengl --write_to_movie -pqh binary_hello.py BinaryToText
    echo.
) else (
    echo.
    echo === Installation Failed ===
    echo.
    echo Try installing manually:
    echo   pip install -r requirements.txt
)

echo NOTE: Environment variables are set for this Command Prompt session only.
echo To make them permanent, add them to your Windows System Environment Variables.
echo.

pause
