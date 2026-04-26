# macOS Tools Bundle GUI

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/Platform-macOS%20|%20Windows%20|%20Linux-purple.svg)]()

**Cross-platform graphical interface for 5 productivity CLI tools** | **5款生产力CLI工具的跨平台图形界面**

---

## 📖 Table of Contents / 目录

- [Overview / 概述](#overview--概述)
- [Features / 特性](#features--特性)
- [Installation / 安装](#installation--安装)
- [Usage Guide / 使用指南](#usage-guide--使用指南)
- [Tool Details / 工具详情](#tool-details--工具详情)
- [Troubleshooting / 故障排除](#troubleshooting--故障排除)
- [Development / 开发](#development--开发)
- [License / 许可证](#license--许可证)

---

## Overview / 概述

### English

macOS Tools Bundle GUI provides a unified graphical interface for 5 command-line productivity tools. Designed for users who prefer visual interfaces over terminal commands, it offers the same powerful functionality with an intuitive dark-themed UI.

**Included Tools:**
- 📝 **SmartRename** — Batch file renaming with 6 patterns (sequence, date, replace, lowercase, uppercase, clean)
- 🖼️ **ImgCrush** — Image compression and HEIC→JPG conversion with quality control
- 📋 **ClipStack** — Clipboard history manager with search and pin support
- 🌳 **DirSnap** — Directory structure snapshots in multiple formats
- 🔐 **EnvGuard** — AES-256-GCM encrypted .env file backup

### 中文

macOS 工具集 GUI 为5款命令行生产力工具提供统一的图形界面。专为偏好可视化操作的用户设计，在直观的深色主题界面下提供同样强大的功能。

**包含工具：**
- 📝 **SmartRename** — 批量文件重命名（6种模式：序列、日期、替换、小写、大写、清理）
- 🖼️ **ImgCrush** — 图片压缩和HEIC转JPG，支持质量控制
- 📋 **ClipStack** — 剪贴板历史管理，支持搜索和固定
- 🌳 **DirSnap** — 目录结构快照，多格式输出
- 🔐 **EnvGuard** — AES-256-GCM加密的.env文件备份

---

## Features / 特性

| Feature | Description (EN) | 描述 (中文) |
|---------|------------------|-------------|
| 🌙 Dark Theme | Modern dark UI design, comfortable for long use | 现代深色UI设计，长时间使用舒适 |
| 🖱️ Drag & Drop | Drop files/folders directly into panels | 直接拖放文件/文件夹到面板 |
| 👁️ Live Preview | See changes before executing operations | 执行前预览变更效果 |
| 📊 Progress Indicators | Visual feedback during long operations | 长操作时的可视化进度反馈 |
| 🔄 Background Processing | Non-blocking UI with threaded operations | 后台处理，界面不卡顿 |
| 🌍 Cross-Platform | Same UI on macOS, Windows, Linux | macOS、Windows、Linux统一界面 |
| 🔗 CLI Integration | Uses same tested backend as CLI tools | 使用与CLI相同的测试后端 |
| 📦 Standalone Package | No Python required for pre-built versions | 预编译版本无需安装Python |

---

## Installation / 安装

### Method 1: Pre-built Packages (Recommended) / 方式1：预编译包（推荐）

**English:** Download the pre-built package for your platform. No Python installation required.

**中文：** 下载适合您平台的预编译包，无需安装Python。

| Platform | Format | Size | Download Link |
|----------|--------|------|---------------|
| macOS (Apple Silicon) | .zip | ~195MB | [Releases](https://github.com/Francisezhang/macos-tools-gui/releases) |
| Windows (x64) | .zip | ~49MB | [Releases](https://github.com/Francisezhang/macos-tools-gui/releases) |
| Linux (x64) | .deb | ~59MB | [Releases](https://github.com/Francisezhang/macos-tools-gui/releases) |

#### macOS Installation / macOS 安装步骤

```bash
# 1. Download macos-tools-bundle.zip
# 2. Unzip and move to Applications
unzip macos-tools-bundle.zip
mv "macOS Tools Bundle.app" /Applications/

# 3. First run - allow unsigned app
# Right-click → Open → Click "Open" in dialog
# 或在终端运行:
open -a "macOS Tools Bundle"
```

#### Windows Installation / Windows 安装步骤

```powershell
# 1. Download windows-bundle.zip
# 2. Unzip to desired location
# 3. Double-click "macOS Tools Bundle.exe"
# 4. If Windows Defender warns, click "More info" → "Run anyway"
```

#### Linux Installation / Linux 安装步骤

```bash
# 1. Download macos-tools.deb
# 2. Install with dpkg
sudo dpkg -i macos-tools.deb

# 3. If missing dependencies:
sudo apt-get install -f

# 4. Run
macos-tools-gui
```

---

### Method 2: Smart Installer / 方式2：智能安装器

**English:** Use our smart installer that auto-detects your environment and installs dependencies.

**中文：** 使用智能安装器，自动检测环境并安装依赖。

```bash
# Clone or download the repository
git clone https://github.com/Francisezhang/macos-tools-gui
cd macos-tools-gui

# Run the smart installer (自动检测环境并安装)
python3 install.py

# After installation, launch:
python3 -m gui.main
```

**What the installer does / 安装器功能：**
- ✓ Detects platform (macOS/Windows/Linux) / 检测平台
- ✓ Checks Python version (requires 3.9+) / 检查Python版本
- ✓ Verifies pip availability / 验证pip可用性
- ✓ Installs PySide6 and Pillow / 安装依赖
- ✓ Validates all imports / 验证导入
- ✓ Creates desktop shortcut / 创建桌面快捷方式

---

### Method 3: Manual Installation / 方式3：手动安装

**English:** For users who prefer full control over the installation process.

**中文：** 适合希望完全控制安装过程的用户。

```bash
# 1. Clone repository / 克隆仓库
git clone https://github.com/Francisezhang/macos-tools-gui
cd macos-tools-gui

# 2. Create virtual environment (optional but recommended) / 创建虚拟环境（可选但推荐）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies / 安装依赖
pip install -e ".[dev]"

# 4. Run / 运行
python -m gui.main
```

---

### System Requirements / 系统要求

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.9 | 3.11+ |
| RAM | 512MB | 2GB+ |
| Disk Space | 250MB | 500MB+ |
| Display | 1024x768 | 1920x1080+ |

**Platform-specific / 平台特定要求：**

- **macOS:** macOS 11.0 (Big Sur) or later
- **Windows:** Windows 10 or later, Visual C++ Redistributable
- **Linux:** Ubuntu 20.04+, Debian 11+, or equivalent; `libxcb-xinerama0` package

---

## Usage Guide / 使用指南

### Launching the Application / 启动应用

#### From Pre-built Package / 从预编译包启动

- **macOS:** Double-click `macOS Tools Bundle.app` in Applications
- **Windows:** Double-click `macOS Tools Bundle.exe`
- **Linux:** Run `macos-tools-gui` from terminal

#### From Source / 从源码启动

```bash
cd macos-tools-gui
python3 -m gui.main
```

---

### Interface Overview / 界面概述

```
┌─────────────────────────────────────────────────────────────┐
│  🛠️ macOS Tools Bundle                              [_][□][×] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │
│  │ 📝   │ │ 🖼️   │ │ 📋   │ │ 🌳   │ │ 🔐   │              │
│  │Rename│ │Crush │ │Clip  │ │Snap  │ │Guard │              │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘              │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Tool Panel                           ││
│  │                                                         ││
│  │   ┌───────────────────────────────────────────────────┐ ││
│  │   │ Options / Settings                                │ ││
│  │   └───────────────────────────────────────────────────┘ ││
│  │                                                         ││
│  │   ┌───────────────────────────────────────────────────┐ ││
│  │   │ Preview / Results                                 │ ││
│  │   └───────────────────────────────────────────────────┘ ││
│  │                                                         ││
│  │   [Preview] [Execute] [Undo]                           ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  Status: Ready                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Keyboard Shortcuts / 快捷键

| Shortcut | Action (EN) | 操作 (中文) |
|----------|-------------|-------------|
| `Ctrl+Q` / `Cmd+Q` | Quit application | 退出程序 |
| `Ctrl+Tab` | Switch to next tool | 切换到下一个工具 |
| `Ctrl+Shift+Tab` | Switch to previous tool | 切换到上一个工具 |
| `Enter` | Execute current operation | 执行当前操作 |
| `Esc` | Cancel / Clear selection | 取消/清除选择 |

---

### General Workflow / 通用工作流程

1. **Select Tool / 选择工具:** Click the tool icon in the sidebar
2. **Configure Options / 配置选项:** Set parameters in the options panel
3. **Preview / 预览:** Click "Preview" to see expected results
4. **Execute / 执行:** Click "Execute" to apply changes
5. **Undo if needed / 如需撤销:** Use "Undo" to revert last operation

---

## Tool Details / 工具详情

### 📝 SmartRename

**English:** Batch rename files with various patterns.

**中文：** 使用多种模式批量重命名文件。

**Patterns / 模式:**

| Pattern | Description (EN) | 描述 (中文) |
|---------|------------------|-------------|
| `sequence` | Number files (001, 002, 003...) | 序列编号 |
| `date` | Add date prefix (2024-01-15_filename) | 添加日期前缀 |
| `replace` | Find and replace text | 查找替换文本 |
| `lowercase` | Convert to lowercase | 转为小写 |
| `uppercase` | Convert to uppercase | 转为大写 |
| `clean` | Remove special characters | 清理特殊字符 |

**Options / 选项:**
- `Start Number` - Starting sequence number (序列起始号)
- `Padding` - Number of digits (位数，如3位: 001)
- `Find/Replace` - Text to find and replace (查找/替换文本)
- `Regex` - Enable regular expressions (启用正则表达式)
- `Recursive` - Include subdirectories (包含子目录)
- `Filter Pattern` - File filter (*.jpg, *.png) (文件过滤)

---

### 🖼️ ImgCrush

**English:** Compress images and convert HEIC to JPG.

**中文：** 压缩图片并将HEIC转换为JPG。

**Operations / 操作:**

| Operation | Description (EN) | 描述 (中文) |
|-----------|------------------|-------------|
| Compress | Reduce image file size | 减小图片文件大小 |
| Convert HEIC | HEIC → JPG conversion | HEIC转JPG |

**Options / 选项:**
- `Quality (10-100%)` - Compression quality level (压缩质量)
- `Max Width` - Resize to max width (调整最大宽度)
- `Filter Pattern` - Target specific files (目标文件过滤)

**Supported Formats / 支持格式:**
- Input: JPG, PNG, HEIC, WebP, GIF, BMP
- Output: JPG, PNG

---

### 📋 ClipStack

**English:** Manage clipboard history with search and organization.

**中文：** 管理剪贴板历史，支持搜索和整理。

**Features / 功能:**
- Auto-record copied content / 自动记录复制内容
- Search history / 搜索历史
- Pin important items / 固定重要内容
- Type detection (URL, Code, Text) / 类型检测
- Daemon mode for background monitoring / 后台守护进程模式

**Actions / 操作:**
| Action | Description (EN) | 描述 (中文) |
|--------|------------------|-------------|
| Copy Selected | Copy entry to clipboard | 复制选中项到剪贴板 |
| Pin/Unpin | Mark as important | 固定/取消固定 |
| Delete | Remove entry | 删除条目 |
| Clear All | Clear history (keeps pinned) | 清空历史（保留固定项) |

---

### 🌳 DirSnap

**English:** Generate directory structure snapshots.

**中文：** 生成目录结构快照。

**Output Formats / 输出格式:**

| Format | Description (EN) | 描述 (中文) |
|--------|------------------|-------------|
| Tree | ASCII tree visualization | ASCII树形图 |
| Markdown | Markdown-formatted list | Markdown格式列表 |
| JSON | JSON data structure | JSON数据结构 |
| HTML | Interactive HTML page | 交互式HTML页面 |

**Options / 选项:**
- `Recursive` - Include all subdirectories / 包含所有子目录
- `Show Hidden` - Include hidden files / 包含隐藏文件
- `Exclude Patterns` - Skip directories (node_modules, .git) / 排除目录

---

### 🔐 EnvGuard

**English:** Secure backup for .env files with AES-256 encryption.

**中文：** AES-256加密的.env文件安全备份。

**Features / 功能:**
- AES-256-GCM encryption / AES-256-GCM加密
- Master password protection / 主密码保护
- Scan for .env files / 扫描.env文件
- Cloud sync support (iCloud/OneDrive/Dropbox) / 云同步支持

**Security / 安全性:**
- Industry-standard encryption / 行业标准加密
- Local storage only / 仅本地存储
- No network transmission / 无网络传输

---

## Troubleshooting / 故障排除

### Common Issues / 常见问题

#### Application won't start / 应用无法启动

**English:**
1. Check Python version: `python3 --version` (need 3.9+)
2. Verify PySide6: `python3 -c "import PySide6; print('OK')"`
3. Reinstall dependencies: `pip install --force-reinstall PySide6`

**中文:**
1. 检查Python版本：`python3 --version`（需要3.9+）
2. 验证PySide6：`python3 -c "import PySide6; print('OK')"`
3. 重新安装依赖：`pip install --force-reinstall PySide6`

#### macOS: Permission denied / macOS：权限被拒绝

```bash
# Allow execution
chmod +x install.py
xattr -cr .  # Remove quarantine attribute
```

#### Windows: Visual C++ error / Windows：Visual C++错误

Download and install: [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

#### Linux: Missing libxcb / Linux：缺少libxcb

```bash
sudo apt-get install libxcb-xinerama0 libxcb-cursor0
```

---

### Getting Help / 获取帮助

| Channel | Description (EN) | 描述 (中文) |
|---------|------------------|-------------|
| GitHub Issues | Report bugs, request features | 报告Bug，请求功能 |
| Discussions | Ask questions, share tips | 提问，分享技巧 |
| Wiki | Detailed documentation | 详细文档 |

**Links:**
- Repository: https://github.com/Francisezhang/macos-tools-gui
- Issues: https://github.com/Francisezhang/macos-tools-gui/issues
- Releases: https://github.com/Francisezhang/macos-tools-gui/releases

---

## Development / 开发

### Project Structure / 项目结构

```
macos-tools-gui/
├── gui/
│   ├── main.py              # Entry point / 入口
│   ├── main_window.py       # Main window / 主窗口
│   ├── panels/              # Tool panels / 工具面板
│   │   ├── smartrename_panel.py
│   │   ├── imgcrush_panel.py
│   │   ├── clipstack_panel.py
│   │   ├── dirsnap_panel.py
│   │   └── envguard_panel.py
│   ├── widgets/             # Custom widgets / 自定义控件
│   │   └── base_panel.py
│   ├── styles/              # Themes / 主题样式
│   │   └ dark_theme.py
│   └── resources/           # Assets / 资源文件
│       └── icons/
├── tests/                   # Test suite / 测试
├── install.py               # Smart installer / 智能安装器
├── pyproject.toml           # Package config / 包配置
├── macos_tools_gui.spec     # PyInstaller config
└── .github/workflows/       # CI/CD
```

### Build from Source / 从源码构建

```bash
# Install build dependencies
pip install pyinstaller pillow

# macOS
pyinstaller macos_tools_gui.spec --clean --noconfirm

# Windows (run on Windows)
pyinstaller macos_tools_gui.spec --clean --noconfirm

# Linux (create .deb)
pyinstaller macos_tools_gui.spec --clean --noconfirm
cd dist
dpkg-deb --build macos-tools
```

---

## License / 许可证

MIT License - Free to use, modify, and distribute.

MIT 许可证 - 免费使用、修改和分发。

---

**Part of [macOS Tools Bundle](https://github.com/Francisezhang/macos-tools-bundle)** | **[macOS 工具集](https://github.com/Francisezhang/macos-tools-bundle)的一部分**