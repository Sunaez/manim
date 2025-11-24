# Windows GPU Setup Script for AMD RX 9060XT
# Run this with: .\setup_gpu.ps1

Write-Host "=== GPU Setup for Manim with AMD RX 9060XT (Windows) ===" -ForegroundColor Cyan
Write-Host ""

# Set AMD GPU environment variables for Windows
$env:MESA_GL_VERSION_OVERRIDE = "4.6"
$env:FORCE_DISCRETE_GPU = "1"

# Windows doesn't use RADV (that's Linux), but we can set other optimizations
# AMD drivers on Windows handle GPU selection automatically

Write-Host "Installing required Python packages..." -ForegroundColor Yellow
Write-Host ""

# Install packages
pip install manim moderngl PyOpenGL PyOpenGL-accelerate numpy

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Installation Complete ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Environment variables set:" -ForegroundColor Cyan
    Write-Host "  MESA_GL_VERSION_OVERRIDE = $env:MESA_GL_VERSION_OVERRIDE"
    Write-Host "  FORCE_DISCRETE_GPU = $env:FORCE_DISCRETE_GPU"
    Write-Host ""
    Write-Host "=== GPU Setup Complete ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  manim --renderer=opengl --write_to_movie -pqh binary_hello.py BinaryToText"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=== Installation Failed ===" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try installing manually:" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt"
}

# Keep environment variables for this session
Write-Host "NOTE: Environment variables are set for this PowerShell session only." -ForegroundColor Yellow
Write-Host "To make them permanent, run this script each time or add them to your system environment." -ForegroundColor Yellow
Write-Host ""
