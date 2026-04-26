@echo off
REM macOS Tools Bundle GUI - Easy Launcher for Windows
REM Double-click to run

cd /d "%~dp0"

REM Check Python
python --version >nul 2>nul
if errorlevel 1 (
    echo Error: Python not found
    echo Please install Python 3.9+ from: https://python.org/downloads/
    pause
    exit /b 1
)

REM Check PySide6
python -c "import PySide6.QtWidgets" >nul 2>nul
if errorlevel 1 (
    echo Installing PySide6...
    python -m pip install PySide6 --quiet
)

REM Launch GUI
echo Launching macOS Tools Bundle GUI...
python -m gui.main

pause