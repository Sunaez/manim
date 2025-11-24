# ManimGL GPU Animations for Windows

Professional animations optimized for **AMD RX 9060XT 16GB** on Windows using **ManimGL** - the original Manim with native OpenGL/GPU support.

## Why ManimGL?

**ManimGL has NATIVE GPU support** - unlike Manim Community Edition, it's built from the ground up for OpenGL rendering:
- ✅ **Native OpenGL** - GPU acceleration is automatic, no flags needed
- ✅ **Better VRAM usage** - Directly uses GPU memory
- ✅ **Faster rendering** - Optimized for graphics cards
- ✅ **Real-time preview** - Interactive window with GPU acceleration
- ✅ **Created by 3Blue1Brown** - The original vision

## Projects

### 1. Binary to Text Animation (`binary_hello.py`)
Visualizes how binary data is read and decoded into the word "Hello".

### 2. GPU Shader Demo (`gpu_shader_demo.py`)
Performance comparison between CPU and GPU rendering with shader effects.

### 3. GPU Compute Demo (`gpu_compute_demo.py`)
**2800+ objects** - Maximum GPU utilization stress test using VRAM.

## Requirements

- **Windows 10/11**
- **Python 3.8+**
- **AMD RX 9060XT 16GB** with latest drivers from AMD.com
- **LaTeX** (TeXworks or MiKTeX) - for text rendering

## Quick Setup (Automatic - No Manual Configuration!)

### Step 1: Install Python Packages

```powershell
pip install manimgl moderngl PyOpenGL PyOpenGL-accelerate numpy pillow
```

### Step 2: One-Time Windows GPU Configuration (Run Once)

**Right-click PowerShell → Run as Administrator**, then:

```powershell
.\configure_windows_gpu.ps1
```

This automatically:
- ✅ Sets system environment variables for VRAM usage
- ✅ Configures AMD GPU heap and allocation settings
- ✅ Opens Windows Graphics Settings for you
- ✅ Makes settings permanent (no need to run again)

**In Graphics Settings:**
1. Click **Browse** → select your `python.exe`
2. Click **Options** → select **High Performance**
3. Click **Save**

### Step 3: Done! You're ready to render.

## Running Animations (Simple!)

Just use the automatic GPU launcher:

### Binary to Text Animation

```powershell
python run_gpu.py binary_hello.py BinaryToText
```

### GPU Compute Demo (2800+ objects using VRAM)

```powershell
python run_gpu.py gpu_compute_demo.py GPUComputeDemo
```

### GPU Shader Demo

```powershell
python run_gpu.py gpu_shader_demo.py GPUShaderDemo
```

The `run_gpu.py` script automatically:
- Sets GPU environment variables
- Configures VRAM allocation
- Runs manimgl (OpenGL is native - no flags needed!)

**ManimGL uses OpenGL by default - GPU acceleration is automatic!**

## Monitoring VRAM Usage

### Task Manager Method (Easiest)

1. Open **Task Manager** (`Ctrl + Shift + Esc`)
2. Go to **Performance** tab
3. Click on **GPU 0** (your AMD RX 9060XT)
4. Watch these metrics during rendering:
   - **Dedicated GPU Memory** (VRAM) - should increase to 2-4 GB
   - **GPU Utilization** - should be 70-100%
   - **GPU 3D** - should spike during particle effects

**What to look for:**
- ✅ **Good**: "Dedicated GPU Memory" increases → using VRAM
- ❌ **Bad**: Only "Shared GPU Memory" increases → using system RAM

### AMD Software Method

1. Open **AMD Software: Adrenalin Edition**
2. Go to **Performance** → **Metrics**
3. Enable overlay for:
   - **GPU Usage**
   - **VRAM Usage**
   - **Temperature**
4. Keep overlay visible while rendering

## Font Style Consistency

The animations use a consistent font system:
- **MathTex**: Mathematical equations and symbols (conversions, checkmark)
- **Tex**: LaTeX-formatted text (`\textbf{}`, `\texttt{}`)
- **Text**: Normal text labels and output

## GPU Configuration Details

### Environment Variables for VRAM Usage

The setup scripts configure these to force VRAM allocation:

```powershell
GPU_MAX_HEAP_SIZE = 100           # Use 100% of GPU heap
GPU_MAX_ALLOC_PERCENT = 100       # Allow 100% VRAM allocation
GPU_SINGLE_ALLOC_PERCENT = 100    # Single allocation can use 100%
FORCE_DISCRETE_GPU = 1            # Force dedicated AMD GPU
MESA_GL_VERSION_OVERRIDE = 4.6    # Force OpenGL 4.6
```

These prevent fallback to system RAM.

## ManimGL Advantages

### Native OpenGL Rendering
- No `--renderer=opengl` flag needed
- OpenGL is the default and only renderer
- Built for GPU from the ground up

### Interactive Preview Window
- Real-time rendering preview
- GPU-accelerated display
- Can interact with animations while they run

### Better Performance
- Optimized for graphics cards
- Direct GPU memory access
- More efficient than Manim Community Edition

## GPU Compute Demo Details

The `gpu_compute_demo.py` is designed to use your 16GB VRAM:

### What It Does:
1. **2000 Particles** with real-time physics
   - Wave motion calculations (sine/cosine)
   - Vortex effects with radial transformations
   - Explosion particle burst

2. **800-Point Fractal** with golden angle spiral
   - Continuous color transformations
   - Rotation and scaling on GPU

3. **Total: 2800+ GPU Objects**
   - All stored in VRAM (not system RAM)
   - All transformed by GPU shaders
   - Parallel processing on thousands of GPU cores

### Expected Performance:
- **VRAM Usage**: 2-4 GB (watch "Dedicated GPU Memory")
- **GPU Utilization**: 70-100% during particle effects
- **Frame Rate**: Smooth 60fps
- **Render Time**: 1-2 minutes
- **System RAM**: Should stay relatively flat

## Troubleshooting

### Issue: Still Using System RAM Instead of VRAM

**Solution 1: Verify environment variables are set**
```powershell
# Check if variables were configured:
[System.Environment]::GetEnvironmentVariable('GPU_MAX_HEAP_SIZE', 'User')
[System.Environment]::GetEnvironmentVariable('GPU_MAX_ALLOC_PERCENT', 'User')

# Both should output "100"
# If not, run configure_windows_gpu.ps1 as Administrator again
```

**Solution 2: Verify Python is set to High Performance**
1. Settings → Display → Graphics Settings
2. Check if `python.exe` is in the list
3. If not, click **Browse**, add `python.exe`
4. Click **Options**, ensure **High Performance** is selected
5. Restart computer

**Solution 3: Disable integrated graphics (if you have both)**
1. Go to BIOS/UEFI (restart, press F2/Del)
2. Find "iGPU" or "Integrated Graphics"
3. Disable it (forces Windows to use AMD only)
4. Save and restart

### Issue: GPU Utilization Still Low

1. **Update AMD drivers**
   - Go to https://www.amd.com/en/support
   - Download latest drivers for RX 9060XT
   - Clean install (select "Factory Reset")

2. **Close AMD Software while rendering**
   - AMD Adrenalin can interfere with rendering
   - Close it before running manimgl

3. **Close background applications**
   - Browsers (especially Chrome)
   - Games
   - Video players
   - Other GPU-intensive apps

4. **Run PowerShell as Administrator**
   - Right-click PowerShell → "Run as Administrator"
   - Run `.\setup_gpu.ps1` again

5. **Check Task Manager shows correct GPU**
   - GPU 0 should be "AMD Radeon RX 9060XT"
   - Not "Intel UHD" or other integrated graphics

### Issue: ModernGL or OpenGL Errors

**Solution 1: Reinstall GPU packages**
```powershell
pip uninstall manimgl moderngl PyOpenGL PyOpenGL-accelerate
pip cache purge
pip install manimgl moderngl PyOpenGL PyOpenGL-accelerate --no-cache-dir
```

**Solution 2: Verify OpenGL support**
```powershell
python check_gpu.py
```

Look for output showing your AMD GPU.

**Solution 3: Update Visual C++ Redistributables**
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install and restart

### Issue: LaTeX Errors

1. Install MiKTeX or TeXworks from https://miktex.org/download
2. Add to PATH:
   - Settings → System → About → Advanced System Settings
   - Environment Variables → System variables → Path → Edit
   - Add: `C:\Program Files\MiKTeX\miktex\bin\x64\`
3. Restart PowerShell

## Command Reference

### Running Animations

```powershell
# Basic usage
python run_gpu.py <script.py> <SceneName>

# Examples
python run_gpu.py binary_hello.py BinaryToText
python run_gpu.py gpu_compute_demo.py GPUComputeDemo
python run_gpu.py gpu_shader_demo.py GPUShaderDemo
```

**Note**: ManimGL renders at optimal quality automatically - no quality flags needed!

## Output Location

Videos are saved to:
```
media\videos\[script_name]\[SceneName].mp4
```

Example:
```
media\videos\gpu_compute_demo\GPUComputeDemo.mp4
```

## Performance Tips

1. **Close AMD Software** during rendering (can interfere)
2. **Close browser** (especially Chrome - uses GPU)
3. **Monitor temps** - GPU should stay under 85°C
4. **Update AMD drivers** from AMD.com (not Windows Update)
5. **Disable Windows Game Bar** if experiencing issues

## Verification Checklist

Before first run:

- [ ] Ran `configure_windows_gpu.ps1` as Administrator (one-time setup)
- [ ] Python.exe set to "High Performance" in Windows Graphics Settings
- [ ] Environment variables are set permanently (check with command in Troubleshooting)
- [ ] AMD drivers updated from AMD.com
- [ ] Task Manager Performance tab open on GPU view

Then run:
```powershell
python run_gpu.py gpu_compute_demo.py GPUComputeDemo
```

Watch Task Manager → Performance → GPU → **"Dedicated GPU Memory"** increase to 2-4 GB during particle animations.

**If VRAM usage looks good, you're all set! No need to configure anything again.**

## Binary Encoding Reference

The word "Hello" in `binary_hello.py`:
- H = 01001000 (72 decimal)
- e = 01100101 (101 decimal)
- l = 01101100 (108 decimal)
- l = 01101100 (108 decimal)
- o = 01101111 (111 decimal)

## Additional Support

If VRAM usage is still not showing:

1. **Verify environment variables are permanently set:**
   ```powershell
   [System.Environment]::GetEnvironmentVariable('GPU_MAX_HEAP_SIZE', 'User')
   [System.Environment]::GetEnvironmentVariable('GPU_MAX_ALLOC_PERCENT', 'User')
   [System.Environment]::GetEnvironmentVariable('FORCE_DISCRETE_GPU', 'User')
   ```
   All should return "100", "100", "1" respectively.

2. **Check Python is using right GPU:**
   - Open Task Manager before running
   - Run: `python check_gpu.py`
   - Watch which GPU spikes in Task Manager
   - Should be GPU 0 (AMD RX 9060XT), not integrated graphics

3. **Confirm ManimGL is using OpenGL:**
   - ManimGL always uses OpenGL - it's the only renderer
   - The `run_gpu.py` script automatically configures environment

4. **Test with simple OpenGL app:**
   ```powershell
   python -c "import moderngl; ctx = moderngl.create_standalone_context(); print(ctx.info)"
   ```
   Should show AMD GPU info, not software renderer.

5. **Force GPU in AMD Software:**
   - Open AMD Software: Adrenalin Edition
   - Gaming → Global Graphics
   - Set "GPU Workload" to "Graphics"
   - Set "Wait for Vertical Refresh" to "Off"

6. **Nuclear option - Reset graphics preferences:**
   ```powershell
   # Run as Administrator
   Remove-Item -Path "HKCU:\Software\Microsoft\DirectX\UserGpuPreferences" -Recurse -Force
   ```
   Then re-run `configure_windows_gpu.ps1` and add Python to Graphics Settings again.

## Why ManimGL Over Manim Community?

**ManimGL is the original Manim created by Grant Sanderson (3Blue1Brown)**:
- Designed for GPU rendering from day one
- OpenGL is the only renderer - simpler and faster
- Active development focused on performance
- Better suited for GPU-heavy animations
- Native VRAM usage without workarounds

**Manim Community Edition:**
- Cairo renderer by default (CPU-only)
- OpenGL support is secondary/experimental
- Requires `--renderer=opengl` flag
- More complex architecture
- Better for compatibility, worse for GPU performance

For your AMD RX 9060XT 16GB, **ManimGL is the better choice** for maximum GPU utilization!
