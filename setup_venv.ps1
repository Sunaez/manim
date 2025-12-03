# Manim CE Virtual Environment Setup Script
# This script creates a dedicated Python virtual environment for Manim

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Manim CE Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCmd) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version
Write-Host "Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check if venv already exists
$venvPath = Join-Path $PSScriptRoot "venv"
if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists at: $venvPath" -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item -Path $venvPath -Recurse -Force
    } else {
        Write-Host "Keeping existing environment. Upgrading packages..." -ForegroundColor Yellow
        & "$venvPath\Scripts\python.exe" -m pip install --upgrade pip
        & "$venvPath\Scripts\python.exe" -m pip install --upgrade -r requirements.txt
        Write-Host ""
        Write-Host "Setup complete!" -ForegroundColor Green
        exit 0
    }
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

if (-not $?) {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    Write-Host "Make sure Python venv module is installed" -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment created successfully!" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& "$venvPath\Scripts\python.exe" -m pip install --upgrade pip

# Install requirements
Write-Host ""
Write-Host "Installing Manim CE (latest version)..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
& "$venvPath\Scripts\python.exe" -m pip install -r requirements.txt

if (-not $?) {
    Write-Host "ERROR: Failed to install requirements" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "Virtual environment created at: $venvPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run animations, use:" -ForegroundColor Yellow
Write-Host "  .\run_manim.bat manim_demo.py ManimFeatureDemo" -ForegroundColor White
Write-Host ""
Write-Host "Or manually activate the environment:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""

# Verify Manim installation
Write-Host "Verifying Manim installation..." -ForegroundColor Yellow
& "$venvPath\Scripts\python.exe" -m manim --version

Write-Host ""
Write-Host "You're ready to create animations!" -ForegroundColor Green
