# Manim GPU Animations for Windows

Professional Manim animations optimized for **AMD RX 9060XT 16GB** on Windows, featuring GPU acceleration with VRAM usage and LaTeX rendering.

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
- **16GB+ System RAM** (recommended)

## Quick Setup

### Step 1: Install Dependencies

Open **PowerShell** in the project directory:

```powershell
# Run the GPU setup script (sets VRAM environment variables)
.\setup_gpu.ps1
```

Or use **Command Prompt**:

```cmd
setup_gpu.bat
```

This will:
- Install Manim and all dependencies
- Install GPU libraries (ModernGL, PyOpenGL)
- Configure AMD GPU environment variables for **VRAM usage** (not system RAM)
- Set up OpenGL acceleration
- Configure heap size and allocation percentages

### Step 2: Verify GPU Setup

```powershell
python check_gpu.py
```

You should see all ✓ checkmarks for installed packages.

### Step 3: Configure Windows Graphics Settings

**Critical:** Force Python to use your AMD GPU.

1. Open **Settings** → **System** → **Display**
2. Scroll down and click **Graphics Settings**
3. Click **Browse** and navigate to `python.exe`
   - Usually: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`
4. Click **Options** and select **High Performance**
5. Click **Save**

## Running Animations

**⚠️ Important:** Always run from the **same PowerShell/CMD window** where you ran the setup script! The environment variables are session-specific.

### Binary to Text Animation

```powershell
manim --renderer=opengl --write_to_movie -pqh binary_hello.py BinaryToText
```

### GPU Compute Demo (Uses VRAM - Watch Task Manager!)

```powershell
manim --renderer=opengl --write_to_movie -pqh gpu_compute_demo.py GPUComputeDemo
```

### GPU Shader Demo

```powershell
manim --renderer=opengl --write_to_movie -pqh gpu_shader_demo.py GPUShaderDemo
```

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
MANIM_RENDERER = opengl           # Use OpenGL renderer
MESA_GL_VERSION_OVERRIDE = 4.6    # Force OpenGL 4.6
```

These prevent fallback to system RAM.

### manim.cfg Settings

```ini
disable_caching = True    # No intermediate files
flush_cache = True        # Clean temporary files
frame_rate = 60          # Smooth 60fps
pixel_height = 1080      # Full HD resolution
```

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

**Solution 1: Check environment variables are set**
```powershell
# In your current PowerShell session:
$env:GPU_MAX_HEAP_SIZE
$env:GPU_MAX_ALLOC_PERCENT

# Should output "100" for both
# If not, run .\setup_gpu.ps1 again
```

**Solution 2: Make environment variables permanent**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to **Advanced** tab → **Environment Variables**
3. Under "User variables", click **New** and add:
   - Variable: `GPU_MAX_HEAP_SIZE`, Value: `100`
   - Variable: `GPU_MAX_ALLOC_PERCENT`, Value: `100`
   - Variable: `GPU_SINGLE_ALLOC_PERCENT`, Value: `100`
   - Variable: `FORCE_DISCRETE_GPU`, Value: `1`
4. Click **OK** and restart PowerShell

**Solution 3: Force GPU in Windows Settings**
1. Settings → Display → Graphics Settings
2. Click **Browse**, add `python.exe`
3. Click **Options**, select **High Performance**
4. Restart computer

**Solution 4: Disable integrated graphics (if applicable)**
1. Go to BIOS/UEFI (restart, press F2/Del)
2. Find "iGPU" or "Integrated Graphics"
3. Disable it (forces Windows to use AMD only)

### Issue: GPU Utilization Still Low

1. **Update AMD drivers**
   - Go to https://www.amd.com/en/support
   - Download latest drivers for RX 9060XT
   - Clean install (select "Factory Reset")

2. **Close AMD Software while rendering**
   - AMD Adrenalin can interfere with rendering
   - Close it before running manim

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
pip uninstall moderngl PyOpenGL PyOpenGL-accelerate
pip cache purge
pip install moderngl PyOpenGL PyOpenGL-accelerate --no-cache-dir
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

### Quality Flags
```powershell
-pql  # Low quality (480p) - Fast preview
-pqm  # Medium quality (720p)
-pqh  # High quality (1080p) - Best for GPU testing
```

### Important Flags
```powershell
--renderer=opengl    # Required for GPU acceleration
--write_to_movie     # Save as video file
-p                   # Play video after rendering
```

### Examples
```powershell
# Quick preview (low quality, fast)
manim --renderer=opengl --write_to_movie -pql gpu_compute_demo.py GPUComputeDemo

# High quality (uses maximum VRAM)
manim --renderer=opengl --write_to_movie -pqh gpu_compute_demo.py GPUComputeDemo

# List all scenes in a file
manim binary_hello.py --list
```

## Output Location

Videos are saved to:
```
media\videos\[script_name]\[quality]\[scene_name].mp4
```

Example:
```
media\videos\gpu_compute_demo\1080p60\GPUComputeDemo.mp4
```

## Performance Tips

1. **Keep PowerShell window open** - Environment variables are session-specific
2. **Close AMD Software** during rendering
3. **Close browser** (especially Chrome - uses GPU)
4. **Use `-pqh`** to push GPU harder
5. **Monitor temps** - GPU should stay under 85°C
6. **Update Windows** to latest version
7. **Update AMD drivers** monthly
8. **Disable Windows Game Bar** (can interfere with GPU)

## Verification Checklist

Before rendering, verify:

- [ ] Ran `.\setup_gpu.ps1` in current PowerShell session
- [ ] All checkmarks in `python check_gpu.py`
- [ ] Python.exe set to "High Performance" in Windows Graphics Settings
- [ ] Task Manager shows AMD RX 9060XT as GPU 0
- [ ] AMD drivers updated from AMD.com (not Windows Update)
- [ ] Running manim from same PowerShell window as setup script
- [ ] Task Manager Performance tab is open on GPU view

Then run:
```powershell
manim --renderer=opengl --write_to_movie -pqh gpu_compute_demo.py GPUComputeDemo
```

Watch Task Manager → Performance → GPU → **"Dedicated GPU Memory"** increase to 2-4 GB during particle animations.

## Binary Encoding Reference

The word "Hello" in `binary_hello.py`:
- H = 01001000 (72 decimal)
- e = 01100101 (101 decimal)
- l = 01101100 (108 decimal)
- l = 01101100 (108 decimal)
- o = 01101111 (111 decimal)

## Additional Support

If VRAM usage is still not showing:

1. **Verify environment variables in current session:**
   ```powershell
   Get-ChildItem Env: | Where-Object {$_.Name -like "*GPU*"}
   ```

2. **Check Python is using right GPU:**
   - Open Task Manager
   - Run: `python check_gpu.py`
   - Watch which GPU spikes

3. **Confirm OpenGL renderer is active:**
   - Look for "Using OpenGL renderer" in manim output
   - If it says "Using Cairo renderer", OpenGL isn't working

4. **Test with simple OpenGL app:**
   ```powershell
   python -c "import moderngl; ctx = moderngl.create_standalone_context(); print(ctx.info)"
   ```
   Should show AMD GPU info.

5. **Last resort - Force GPU globally:**
   - AMD Radeon Settings → Graphics → Advanced
   - Set "GPU Workload" to "Graphics"
   - Set "Wait for Vertical Refresh" to "Off"
