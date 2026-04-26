@echo off
REM macOS Tools Bundle GUI - Windows Smart Installer
REM Auto-detect environment and install dependencies

echo.
echo ================================================================
echo     macOS Tools Bundle GUI - Smart Installer v1.0
echo     Cross-platform GUI for 5 productivity tools
echo ================================================================
echo.

REM Check Python version
echo [CHECK] Detecting Python version...
python --version 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo [INFO] Please install Python 3.9+ from: https://python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check Python version is 3.9+
for /f "tokens=2" %%i in ('python --version 2^>nul') do set PYTHON_VERSION=%%i
echo [OK] Python version: %PYTHON_VERSION%

REM Check pip
echo [CHECK] Checking pip availability...
python -m pip --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] pip not available!
    echo [INFO] Try: python -m ensurepip
    pause
    exit /b 1
)
echo [OK] pip available

REM Install PySide6
echo [INSTALL] Installing PySide6...
python -m pip install PySide6 --quiet
if errorlevel 1 (
    echo [WARN] PySide6 installation may have issues
    echo [INFO] Try manual install: pip install PySide6
) else (
    echo [OK] PySide6 installed
)

REM Install Pillow (optional)
echo [INSTALL] Installing Pillow (optional)...
python -m pip install Pillow --quiet 2>nul
if errorlevel 1 (
    echo [WARN] Pillow installation skipped
) else (
    echo [OK] Pillow installed
)

REM Verify installation
echo [VERIFY] Verifying installation...
python -c "import PySide6.QtWidgets; print('[OK] PySide6.QtWidgets')" 2>nul
python -c "import PySide6.QtCore; print('[OK] PySide6.QtCore')" 2>nul
python -c "import PySide6.QtGui; print('[OK] PySide6.QtGui')" 2>nul

REM Check GUI package
echo [CHECK] Checking GUI package...
python -c "import sys; sys.path.insert(0, '.'); from gui.main_window import MainWindow; print('[OK] GUI package')" 2>nul
if errorlevel 1 (
    echo [WARN] GUI package not found in current directory
    echo [INFO] Run this installer from the gui directory
)

echo.
echo ================================================================
echo                    Installation Complete!
echo ================================================================
echo.
echo To launch the GUI:
echo   python -m gui.main
echo.
echo Or double-click: launch_gui.bat
echo.
pause