# macOS Tools Bundle GUI

**Cross-platform graphical interface for 5 CLI tools**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

## Overview

This GUI provides a unified launcher for the macOS Tools Bundle CLI tools, making them accessible to users who prefer graphical interfaces over command-line.

**Included Tools:**
- 📝 **SmartRename** — Batch file renaming with 6 patterns
- 🖼️ **ImgCrush** — Image compression and HEIC conversion
- 📋 **ClipStack** — Clipboard history manager
- 🌳 **DirSnap** — Directory structure snapshots
- 🔐 **EnvGuard** — Encrypted .env backup

## Screenshots

```
┌─────────────────────────────────────────────┐
│  🛠️ macOS Tools Bundle                     │
├─────────────────────────────────────────────┤
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐│
│  │ 📝   │ │ 🖼️   │ │ 📋   │ │ 🌳   │ │ 🔐   ││
│  │Rename│ │Crush │ │Clip  │ │Snap  │ │Guard ││
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘│
│                                             │
│  ┌─────────────────────────────────────────┐│
│  │         Tool Panel Content              ││
│  │                                         ││
│  └─────────────────────────────────────────┘│
└─────────────────────────────────────────────┘
```

## Installation

### From Source

```bash
# Clone repository
git clone https://github.com/Francisezhang/macos-tools-bundle
cd macos-tools-bundle/gui

# Install dependencies
pip install -e .

# Run
python -m gui.main
```

### Pre-built Packages

| Platform | Format | Download |
|----------|--------|----------|
| macOS | .app bundle | [Releases](https://github.com/Francisezhang/macos-tools-bundle/releases) |
| Windows | .exe installer | [Releases](https://github.com/Francisezhang/macos-tools-bundle/releases) |
| Linux | .deb package | [Releases](https://github.com/Francisezhang/macos-tools-bundle/releases) |

## Development

### Requirements

- Python 3.9+
- PySide6 6.6+

### Project Structure

```
gui/
├── gui/
│   ├── main.py              # Entry point
│   ├── main_window.py       # Main window
│   ├── panels/              # Tool panels
│   │   ├── smartrename_panel.py
│   │   ├── imgcrush_panel.py
│   │   ├── dirsnap_panel.py
│   │   ├── clipstack_panel.py
│   │   └── envguard_panel.py
│   ├── widgets/             # Custom widgets
│   ├── styles/              # Theme and styling
│   └── utils/               # Utilities
├── tests/
├── resources/               # Icons, assets
├── pyproject.toml
├── macos_tools_gui.spec     # PyInstaller config
└── .github/workflows/       # CI/CD
```

### Build Locally

```bash
# macOS
pyinstaller macos_tools_gui.spec --clean

# Windows
pyinstaller macos_tools_gui.spec --clean

# Linux
pyinstaller macos_tools_gui.spec --clean
dpkg-deb --build dist/macos-tools
```

## Features

- **Dark Theme**: Modern dark UI design
- **Drag & Drop**: Drop files directly into panels
- **Live Preview**: See changes before executing
- **Progress Indicators**: Visual feedback during operations
- **Keyboard Shortcuts**: Quick actions (future)
- **Cross-Platform**: Same UI on macOS, Windows, Linux

## Architecture

The GUI is a thin wrapper over the CLI backends:

```
GUI (PySide6) → CLI Backend (Python modules) → File System
```

No logic duplication — all operations use the same tested CLI code.

## License

MIT License — Free to use, modify, and distribute.

---

**Part of [macOS Tools Bundle](https://github.com/Francisezhang/macos-tools-bundle)**