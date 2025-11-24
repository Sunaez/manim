# Windows Setup Guide for AMD RX 9060XT

Quick setup guide for Windows users with AMD RX 9060XT graphics cards.

## Prerequisites

1. **Python 3.8+** installed
   - Download from: https://www.python.org/downloads/
   - Make sure "Add Python to PATH" is checked during installation

2. **AMD Drivers** (latest version)
   - Download from: https://www.amd.com/en/support
   - Install AMD Software: Adrenalin Edition

3. **LaTeX** (for text rendering)
   - Download TeXworks or MiKTeX from: https://www.tug.org/texlive/windows.html

## Installation Steps

### Step 1: Open PowerShell in the project directory

```powershell
cd C:\Users\YourUsername\Documents\GitHub\manim
```

### Step 2: Run the GPU setup script

```powershell
.\setup_gpu.ps1
```

This will:
- Install Manim and all dependencies
- Install GPU libraries (ModernGL, PyOpenGL)
- Set up environment variables for GPU acceleration

### Step 3: Verify installation

```powershell
python check_gpu.py
```

You should see:
```
✓ manim is installed
✓ moderngl is installed
✓ PyOpenGL is installed
✓ numpy is installed
```

## Running Animations

### Basic Example (Binary to Text)

```powershell
manim --renderer=opengl --write_to_movie -pqh binary_hello.py BinaryToText
```

### GPU Stress Test (2800+ objects)

```powershell
manim --renderer=opengl --write_to_movie -pqh gpu_compute_demo.py GPUComputeDemo
```

## Monitoring GPU Usage

### Option 1: Task Manager
1. Press `Ctrl + Shift + Esc`
2. Go to **Performance** tab
3. Click on **GPU**
4. Watch utilization while rendering

### Option 2: AMD Software
1. Open **AMD Software: Adrenalin Edition**
2. Go to **Performance** -> **Metrics**
3. Monitor GPU usage, VRAM, and temperature

## Common Issues & Solutions

### Issue: "manim: command not found"

**Solution:**
```powershell
pip install manim
# or
python -m pip install manim
```

### Issue: GPU not being used (low utilization)

**Solution 1:** Configure Windows Graphics Settings
1. Open **Settings** -> **System** -> **Display**
2. Scroll down to **Graphics Settings**
3. Click **Browse** and add `python.exe`
4. Click **Options** and select **High Performance**
5. Click **Save**

**Solution 2:** Check AMD Software
1. Open **AMD Software: Adrenalin Edition**
2. Go to **Gaming** -> **Global Graphics**
3. Ensure GPU Workload is set to **Graphics**

**Solution 3:** Run PowerShell as Administrator
```powershell
# Right-click PowerShell -> "Run as Administrator"
.\setup_gpu.ps1
```

### Issue: ModernGL errors

**Solution:** Update graphics drivers
1. Go to https://www.amd.com/en/support
2. Download latest AMD drivers for RX 9060XT
3. Install and restart computer

### Issue: LaTeX not found

**Solution:** Install TeXworks or MiKTeX
1. Download from: https://www.tug.org/texlive/windows.html
2. Install and add to PATH
3. Restart PowerShell

## Performance Tips

1. **Close background applications** before rendering
2. **Use `-pqh` flag** for high quality (tests GPU more)
3. **Monitor temperatures** with AMD Software
4. **Update drivers** regularly from AMD.com
5. **Enable SAM** (Smart Access Memory) in BIOS if available

## Expected Performance

With proper GPU acceleration:
- **GPU Utilization**: 70-100% during particle effects
- **VRAM Usage**: 2-4 GB for complex animations
- **Frame Rate**: Smooth 60fps with OpenGL renderer
- **Render Time**: 1-2 minutes for gpu_compute_demo.py

## Verification

To verify GPU is being used:

1. Run an animation:
   ```powershell
   manim --renderer=opengl --write_to_movie -pqh gpu_compute_demo.py GPUComputeDemo
   ```

2. Open Task Manager (Ctrl+Shift+Esc)

3. Check GPU usage - should spike to 70-100% during:
   - Particle wave simulations
   - Vortex effects
   - Fractal generation

4. Check VRAM - should see 2-4 GB used

## Need Help?

If you're still experiencing issues:

1. Check that Python is using the AMD GPU:
   ```powershell
   python check_gpu.py
   ```

2. Verify AMD drivers are installed:
   - Open AMD Software: Adrenalin Edition
   - Check driver version

3. Make sure you ran `.\setup_gpu.ps1` in your current PowerShell session

4. Try running PowerShell as Administrator

## Environment Variables

The setup script sets these for your session:
- `MESA_GL_VERSION_OVERRIDE=4.6` - Forces OpenGL 4.6
- `FORCE_DISCRETE_GPU=1` - Prefers dedicated GPU

To make these permanent:
1. Search for "Environment Variables" in Windows
2. Click "Edit system environment variables"
3. Click "Environment Variables" button
4. Add the variables under "User variables"
