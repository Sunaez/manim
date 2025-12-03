@echo off
REM Manim CE Runner - Runs manim using the virtual environment
REM Usage: run_manim.bat <script.py> <SceneName> [additional options]
REM Example: run_manim.bat manim_demo.py ManimFeatureDemo -pqm

setlocal

REM Check if virtual environment exists
if not exist "%~dp0venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup_venv.bat first to create the environment.
    echo.
    pause
    exit /b 1
)

REM Check if arguments provided
if "%~1"=="" (
    echo Usage: run_manim.bat ^<script.py^> ^<SceneName^> [options]
    echo.
    echo Examples:
    echo   run_manim.bat manim_demo.py ManimFeatureDemo -pqm
    echo   run_manim.bat manim_demo.py ManimFeatureDemo -pqh
    echo.
    echo Quality options:
    echo   -pql  = Preview, low quality (480p, 15fps)
    echo   -pqm  = Preview, medium quality (720p, 30fps) [RECOMMENDED]
    echo   -pqh  = Preview, high quality (1080p, 60fps)
    echo   -pqk  = Preview, 4K quality (2160p, 60fps)
    echo.
    pause
    exit /b 1
)

echo =====================================
echo Manim CE - Running Animation
echo =====================================
echo.
echo Using virtual environment: %~dp0venv
echo Script: %1
echo Scene: %2
echo.

REM Run manim using the virtual environment
"%~dp0venv\Scripts\python.exe" -m manim %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =====================================
    echo Rendering failed!
    echo =====================================
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo =====================================
echo Rendering complete!
echo =====================================
echo.
echo Video saved to: media\videos\
echo.
pause
