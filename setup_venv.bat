@echo off
REM Manim CE Virtual Environment Setup - Batch Wrapper
REM This runs the PowerShell setup script

echo Running Manim CE setup script...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0setup_venv.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Setup failed. Please check the error messages above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
pause
