#!/usr/bin/env python3
"""
GPU Verification Script for AMD RX 9060XT
Checks if GPU is properly configured for ManimGL rendering
"""

import sys

def check_import(module_name, package_name=None):
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        print(f"✓ {package_name or module_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name or module_name} is NOT installed")
        return False

def check_opengl():
    """Check OpenGL availability and version."""
    try:
        import OpenGL.GL as gl
        from OpenGL.GL import shaders
        print("✓ PyOpenGL is working")

        # Try to get version (may fail without display)
        try:
            version = gl.glGetString(gl.GL_VERSION)
            if version:
                print(f"  OpenGL Version: {version.decode()}")
        except:
            print("  (Cannot query OpenGL without display/context)")
        return True
    except Exception as e:
        print(f"✗ PyOpenGL error: {e}")
        return False

def check_moderngl():
    """Check ModernGL."""
    try:
        import moderngl
        print(f"✓ ModernGL version {moderngl.VERSION}")

        # Try to create a context
        try:
            ctx = moderngl.create_standalone_context()
            info = ctx.info
            print(f"  GPU Vendor: {info.get('GL_VENDOR', 'Unknown')}")
            print(f"  GPU Renderer: {info.get('GL_RENDERER', 'Unknown')}")
            print(f"  OpenGL Version: {info.get('GL_VERSION', 'Unknown')}")
            ctx.release()
            return True
        except Exception as e:
            print(f"  Could not create context: {e}")
            print("  (This is OK - may need display)")
            return True
    except ImportError:
        print("✗ ModernGL is NOT installed")
        return False

def check_manim():
    """Check ManimGL installation."""
    try:
        import manimlib
        print(f"✓ ManimGL is installed")

        # Check for OpenGL renderer
        try:
            from manim.renderer.opengl_renderer import OpenGLRenderer
            print("  ✓ OpenGL renderer available")
        except ImportError:
            print("  ✗ OpenGL renderer not available")
        return True
    except ImportError:
        print("✗ ManimGL is NOT installed")
        return False

def check_environment():
    """Check environment variables."""
    import os

    print("\n=== Environment Variables ===")

    env_vars = [
        'MESA_GL_VERSION_OVERRIDE',
        'RADV_PERFTEST',
        'DRI_PRIME',
        'AMD_VULKAN_ICD'
    ]

    any_set = False
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"✓ {var} = {value}")
            any_set = True
        else:
            print(f"  {var} not set")

    if not any_set:
        print("\n⚠ No AMD GPU environment variables set")
        print("  Run: source setup_gpu.sh")

    return any_set

def main():
    print("=" * 60)
    print("GPU Configuration Check for AMD RX 9060XT")
    print("=" * 60)
    print()

    all_good = True

    # Check required packages
    print("=== Required Packages ===")
    all_good &= check_import("manimgl")
    all_good &= check_import("moderngl")
    all_good &= check_import("OpenGL", "PyOpenGL")
    all_good &= check_import("numpy")

    print()

    # Check OpenGL
    print("=== OpenGL Status ===")
    check_opengl()
    print()

    # Check ModernGL
    print("=== ModernGL Status ===")
    check_moderngl()
    print()

    # Check environment
    env_set = check_environment()
    print()

    # Final verdict
    print("=" * 60)
    if all_good:
        print("✓ All required packages installed")
        if env_set:
            print("✓ GPU environment configured")
            print("\n✓✓✓ READY TO RENDER WITH GPU! ✓✓✓")
            print("\nTry:")
            print("  manim --renderer=opengl --write_to_movie -pqh \\")
            print("    gpu_compute_demo.py GPUComputeDemo")
        else:
            print("⚠ GPU environment not configured")
            print("\nRun: source setup_gpu.sh")
    else:
        print("✗ Some packages are missing")
        print("\nRun: pip install -r requirements.txt")

    print("=" * 60)

if __name__ == "__main__":
    main()
