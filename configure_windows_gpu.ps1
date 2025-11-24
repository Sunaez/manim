# Automatic Windows GPU Configuration for Python
# This script configures Windows to always use AMD GPU for Python
# Run as Administrator: Right-click PowerShell -> Run as Administrator

Write-Host "=== Configuring Windows for AMD RX 9060XT with ManimGL ===" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "Administrator privileges confirmed." -ForegroundColor Green
Write-Host ""

# Find Python executable
Write-Host "Searching for Python installation..." -ForegroundColor Yellow

$pythonPaths = @()

# Common Python locations
$searchPaths = @(
    "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
    "$env:APPDATA\Local\Programs\Python\Python*\python.exe",
    "C:\Python*\python.exe",
    "$env:ProgramFiles\Python*\python.exe",
    "$env:ProgramFiles(x86)\Python*\python.exe"
)

foreach ($pattern in $searchPaths) {
    $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
    if ($found) {
        $pythonPaths += $found.FullName
    }
}

# Also check PATH
$pathPython = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pathPython) {
    $pythonPaths += $pathPython
}

# Remove duplicates
$pythonPaths = $pythonPaths | Select-Object -Unique

if ($pythonPaths.Count -eq 0) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Found Python installations:" -ForegroundColor Green
for ($i = 0; $i -lt $pythonPaths.Count; $i++) {
    Write-Host "  [$i] $($pythonPaths[$i])" -ForegroundColor White
}
Write-Host ""

# If multiple Python versions found, let user choose
$pythonExe = $pythonPaths[0]
if ($pythonPaths.Count -gt 1) {
    Write-Host "Multiple Python installations found. Using: $pythonExe" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Configuring Python to use AMD GPU..." -ForegroundColor Yellow
Write-Host ""

# Set system environment variables for AMD GPU
Write-Host "Setting system environment variables..." -ForegroundColor Cyan

$envVars = @{
    'GPU_MAX_HEAP_SIZE' = '100'
    'GPU_MAX_ALLOC_PERCENT' = '100'
    'GPU_SINGLE_ALLOC_PERCENT' = '100'
    'FORCE_DISCRETE_GPU' = '1'
}

foreach ($var in $envVars.GetEnumerator()) {
    [System.Environment]::SetEnvironmentVariable($var.Key, $var.Value, [System.EnvironmentVariableTarget]::User)
    Write-Host "  Set $($var.Key) = $($var.Value)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Configuration Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Environment variables have been set permanently." -ForegroundColor Cyan
Write-Host "Python: $pythonExe" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Close this PowerShell window" -ForegroundColor White
Write-Host "  2. Open a NEW PowerShell window" -ForegroundColor White
Write-Host "  3. Go to Windows Settings -> Display -> Graphics Settings" -ForegroundColor White
Write-Host "  4. Add Python.exe and set to 'High Performance'" -ForegroundColor White
Write-Host "  5. Run: python run_gpu.py gpu_compute_demo.py GPUComputeDemo -pqh" -ForegroundColor White
Write-Host ""
Write-Host "After running animations, check Task Manager:" -ForegroundColor Cyan
Write-Host "  Performance -> GPU -> Dedicated GPU Memory (should show 2-4 GB)" -ForegroundColor White
Write-Host ""

# Offer to open Graphics Settings
Write-Host "Would you like to open Windows Graphics Settings now? (Y/N)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Start-Process "ms-settings:display-advancedgraphics"
    Write-Host ""
    Write-Host "Graphics Settings opened!" -ForegroundColor Green
    Write-Host "Add $pythonExe and set to 'High Performance'" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
pause
