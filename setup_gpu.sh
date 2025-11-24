#!/bin/bash
# GPU Setup Script for AMD RX 9060XT

echo "=== GPU Setup for Manim with AMD RX 9060XT ==="

# Set AMD GPU environment variables
export MESA_GL_VERSION_OVERRIDE=4.6
export MESA_GLSL_VERSION_OVERRIDE=460
export AMD_VULKAN_ICD=RADV
export RADV_PERFTEST=aco,ngg
export vk_xwayland_wait_ready=false

# Force GPU acceleration
export __GLX_VENDOR_LIBRARY_NAME=mesa
export DRI_PRIME=1

# OpenGL settings for better performance
export LIBGL_DRI3_DISABLE=0
export LIBGL_ALWAYS_INDIRECT=0

# Disable V-Sync for better performance
export vblank_mode=0

# Show GPU info
echo ""
echo "Environment variables set for AMD GPU acceleration:"
echo "  MESA_GL_VERSION_OVERRIDE=$MESA_GL_VERSION_OVERRIDE"
echo "  RADV_PERFTEST=$RADV_PERFTEST"
echo "  DRI_PRIME=$DRI_PRIME"
echo ""

# Install requirements if needed
if ! python3 -c "import moderngl" 2>/dev/null; then
    echo "Installing GPU acceleration dependencies..."
    pip install -r requirements.txt
else
    echo "GPU dependencies already installed"
fi

echo ""
echo "=== GPU Setup Complete ==="
echo ""
echo "Usage:"
echo "  source setup_gpu.sh"
echo "  manim --renderer=opengl --write_to_movie -pqh binary_hello.py BinaryToText"
echo ""
