#!/bin/bash
# macOS Tools Bundle GUI - Easy Launcher
# 双击运行或在终端执行此脚本启动GUI

cd "$(dirname "$0")"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 not found"
    echo "Please install Python 3.9+ from: https://python.org/downloads/"
    exit 1
fi

# Check PySide6
if ! python3 -c "import PySide6.QtWidgets" 2>/dev/null; then
    echo "PySide6 not installed. Installing..."
    python3 -m pip install PySide6 --quiet
fi

# Launch GUI
echo "Launching macOS Tools Bundle GUI..."
python3 -m gui.main