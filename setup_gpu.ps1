# Windows GPU Setup Script for AMD RX 9060XT
# Run this with: .\setup_gpu.ps1

Write-Host "=== AMD RX 9060XT GPU Setup for ManimGL (Windows) ===" -ForegroundColor Cyan
Write-Host ""

# Set AMD GPU environment variables for Windows
$env:MESA_GL_VERSION_OVERRIDE = "4.6"
$env:FORCE_DISCRETE_GPU = "1"

# AMD-specific settings for VRAM usage
$env:GPU_MAX_HEAP_SIZE = "100"
$env:GPU_MAX_ALLOC_PERCENT = "100"
$env:GPU_SINGLE_ALLOC_PERCENT = "100"

# Disable fallback to CPU
$env:PYOPENGL_FULL_TRACE = "0"

Write-Host "Installing required Python packages..." -ForegroundColor Yellow
Write-Host ""

# Install packages with specific versions for Windows
pip install --upgrade pip
pip install manimgl moderngl PyOpenGL PyOpenGL-accelerate numpy pillow

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Installation Complete ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Environment variables set for GPU VRAM usage:" -ForegroundColor Cyan
    Write-Host "  MESA_GL_VERSION_OVERRIDE = $env:MESA_GL_VERSION_OVERRIDE" -ForegroundColor White
    Write-Host "  FORCE_DISCRETE_GPU = $env:FORCE_DISCRETE_GPU" -ForegroundColor White
    Write-Host "  GPU_MAX_HEAP_SIZE = $env:GPU_MAX_HEAP_SIZE" -ForegroundColor White
    Write-Host "  GPU_MAX_ALLOC_PERCENT = $env:GPU_MAX_ALLOC_PERCENT" -ForegroundColor White
    Write-Host ""
    Write-Host "=== ManimGL Setup Complete ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "ManimGL uses OpenGL natively - GPU acceleration is automatic!" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Close AMD Software: Adrenalin Edition if running" -ForegroundColor White
    Write-Host "  2. Make sure no other apps are using GPU" -ForegroundColor White
    Write-Host "  3. Run: python check_gpu.py" -ForegroundColor White
    Write-Host "  4. Run: python run_gpu.py gpu_compute_demo.py GPUComputeDemo" -ForegroundColor White
    Write-Host ""
    Write-Host "Monitor VRAM usage in Task Manager -> Performance -> GPU -> Dedicated GPU Memory" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=== Installation Failed ===" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try installing manually:" -ForegroundColor Yellow
    Write-Host "  pip install manim moderngl PyOpenGL PyOpenGL-accelerate numpy" -ForegroundColor White
}

Write-Host ""
Write-Host "IMPORTANT: These environment variables are set for this PowerShell session only." -ForegroundColor Yellow
Write-Host "To use them, keep this PowerShell window open and run manim from here." -ForegroundColor Yellow
Write-Host ""
