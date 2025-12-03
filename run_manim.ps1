# Manim CE Runner - PowerShell Version
# Usage: .\run_manim.ps1 <script.py> <SceneName> [additional options]
# Example: .\run_manim.ps1 manim_demo.py ManimFeatureDemo -pqm

param(
    [Parameter(Position=0)]
    [string]$Script,

    [Parameter(Position=1)]
    [string]$Scene,

    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$AdditionalArgs
)

# Check if virtual environment exists
$venvPath = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
if (-not (Test-Path $venvPath)) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run setup_venv.bat first to create the environment." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Show usage if no arguments
if (-not $Script -or -not $Scene) {
    Write-Host "Usage: .\run_manim.ps1 <script.py> <SceneName> [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\run_manim.ps1 manim_demo.py ManimFeatureDemo -pqm" -ForegroundColor White
    Write-Host "  .\run_manim.ps1 manim_demo.py ManimFeatureDemo -pqh" -ForegroundColor White
    Write-Host ""
    Write-Host "Quality options:" -ForegroundColor Cyan
    Write-Host "  -pql  = Preview, low quality (480p, 15fps)" -ForegroundColor White
    Write-Host "  -pqm  = Preview, medium quality (720p, 30fps) [RECOMMENDED]" -ForegroundColor Green
    Write-Host "  -pqh  = Preview, high quality (1080p, 60fps)" -ForegroundColor White
    Write-Host "  -pqk  = Preview, 4K quality (2160p, 60fps)" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Manim CE - Running Animation" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Using virtual environment: $PSScriptRoot\venv" -ForegroundColor Gray
Write-Host "Script: $Script" -ForegroundColor Gray
Write-Host "Scene: $Scene" -ForegroundColor Gray
Write-Host ""

# Build command arguments
$args = @($Script, $Scene) + $AdditionalArgs

# Run manim using the virtual environment
& $venvPath -m manim $args

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Red
    Write-Host "Rendering failed!" -ForegroundColor Red
    Write-Host "=====================================" -ForegroundColor Red
    Write-Host ""
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Rendering complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Video saved to: media\videos\" -ForegroundColor Cyan
Write-Host ""
