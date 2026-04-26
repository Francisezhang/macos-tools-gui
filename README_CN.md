# macOS 工具集 GUI

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/平台-macOS%20|%20Windows%20|%20Linux-purple.svg)]()

**5款生产力CLI工具的跨平台图形界面**

---

## 📖 目录

- [概述](#概述)
- [特性](#特性)
- [安装](#安装)
- [使用指南](#使用指南)
- [工具详情](#工具详情)
- [故障排除](#故障排除)
- [开发](#开发)
- [许可证](#许可证)

---

## 概述

macOS 工具集 GUI 为5款命令行生产力工具提供统一的图形界面。专为偏好可视化操作的用户设计，在直观的深色主题界面下提供同样强大的功能。

**包含工具：**

| 工具 | 功能 | 描述 |
|------|------|------|
| 📝 **SmartRename** | 批量重命名 | 6种模式：序列、日期、替换、大小写、清理 |
| 🖼️ **ImgCrush** | 图片压缩 | 调整质量、HEIC转JPG、批量处理 |
| 📋 **ClipStack** | 剪贴板历史 | 自动记录、搜索、固定、类型识别 |
| 🌳 **DirSnap** | 目录快照 | Tree/Markdown/JSON/HTML多格式输出 |
| 🔐 **EnvGuard** | .env备份 | AES-256加密、云同步支持 |

---

## 特性

| 特性 | 说明 |
|------|------|
| 🌙 **深色主题** | 现代深色UI设计，长时间使用不疲劳 |
| 🖱️ **拖拽支持** | 直接拖放文件/文件夹到面板 |
| 👁️ **实时预览** | 执行前查看变更效果 |
| 📊 **进度指示** | 长操作时的可视化进度反馈 |
| 🔄 **后台处理** | 后台线程处理，界面不卡顿 |
| 🌍 **跨平台** | macOS、Windows、Linux统一界面 |
| 🔗 **CLI集成** | 使用与CLI相同的测试后端 |
| 📦 **独立包** | 预编译版本无需安装Python |

---

## 安装

### 方式一：预编译包（推荐）

下载适合您平台的预编译包，无需安装Python。

| 平台 | 格式 | 大小 | 下载链接 |
|------|------|------|----------|
| macOS (Apple Silicon) | .zip | ~195MB | [Releases](https://github.com/Francisezhang/macos-tools-gui/releases) |
| macOS (Intel) | .zip | ~195MB | [Releases](https://github.com/Francisezhang/macos-tools-gui/releases) |
| Windows (x64) | .zip | ~49MB | [Releases](https://github.com/Francisezhang/macos-tools-gui/releases) |
| Linux (x64) | .deb | ~59MB | [Releases](https://github.com/Francisezhang/macos-tools-gui/releases) |

#### macOS 安装步骤

```bash
# 1. 下载 macos-tools-bundle.zip
# 2. 解压并移动到 Applications
unzip macos-tools-bundle.zip
mv "macOS Tools Bundle.app" /Applications/

# 3. 首次运行 - 允许未签名应用
# 右键点击 → 打开 → 点击对话框中的"打开"
# 或在终端运行:
open -a "macOS Tools Bundle"

# 4. 如果提示权限问题
xattr -cr "/Applications/macOS Tools Bundle.app"
```

#### Windows 安装步骤

```powershell
# 1. 下载 windows-bundle.zip
# 2. 解压到任意位置
Expand-Archive windows-bundle.zip -DestinationPath C:\Tools

# 3. 双击运行 "macOS Tools Bundle.exe"
# 4. 如果Windows Defender警告:
#    点击"更多信息" → "仍要运行"

# 5. 如需添加到开始菜单，右键exe → 创建快捷方式
```

#### Linux 安装步骤

```bash
# 1. 下载 macos-tools.deb
wget https://github.com/Francisezhang/macos-tools-gui/releases/latest/download/macos-tools.deb

# 2. 安装
sudo dpkg -i macos-tools.deb

# 3. 如果缺少依赖:
sudo apt-get install -f

# 4. 运行
macos-tools-gui

# 5. 如需安装桌面图标:
cp /usr/share/applications/macos-tools-gui.desktop ~/Desktop/
```

---

### 方式二：智能安装器

使用智能安装器，自动检测环境并安装依赖。

```bash
# 克隆仓库
git clone https://github.com/Francisezhang/macos-tools-gui
cd macos-tools-gui

# 运行智能安装器
python3 install.py

# 安装完成后启动
python3 -m gui.main
```

**安装器功能：**
- ✓ 自动检测平台 (macOS/Windows/Linux)
- ✓ 检查Python版本 (需要3.9+)
- ✓ 验证pip可用性
- ✓ 自动安装PySide6和Pillow
- ✓ 验证所有模块导入
- ✓ 创建桌面快捷方式

---

### 方式三：手动安装

适合希望完全控制安装过程的用户。

```bash
# 1. 克隆仓库
git clone https://github.com/Francisezhang/macos-tools-gui
cd macos-tools-gui

# 2. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或: venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -e ".[dev]"

# 4. 运行
python -m gui.main
```

---

### 系统要求

| 要求 | 最低 | 推荐 |
|------|------|------|
| Python | 3.9 | 3.11+ |
| 内存 | 512MB | 2GB+ |
| 磁盘空间 | 250MB | 500MB+ |
| 显示器 | 1024x768 | 1920x1080+ |

**平台特定要求：**

- **macOS:** macOS 11.0 (Big Sur) 或更高版本
- **Windows:** Windows 10 或更高版本，需要 Visual C++ Redistributable
- **Linux:** Ubuntu 20.04+、Debian 11+ 或同等版本；需要 `libxcb-xinerama0` 包

---

## 使用指南

### 启动应用

**预编译包：**
- macOS: 双击 Applications 中的 `macOS Tools Bundle.app`
- Windows: 双击 `macOS Tools Bundle.exe`
- Linux: 终端运行 `macos-tools-gui`

**源码安装：**
```bash
cd macos-tools-gui
python3 -m gui.main
```

### 界面布局

```
┌─────────────────────────────────────────────────────────────┐
│  🛠️ macOS 工具集                                     [_][□][×] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │
│  │ 📝   │ │ 🖼️   │ │ 📋   │ │ 🌳   │ │ 🔐   │  ← 工具栏   │
│  │Rename│ │Crush │ │Clip  │ │Snap  │ │Guard │              │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘              │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    工具面板                             ││
│  │                                                         ││
│  │   ┌───────────────────────────────────────────────────┐ ││
│  │   │ 选项设置                                          │ ││
│  │   └───────────────────────────────────────────────────┘ ││
│  │                                                         ││
│  │   ┌───────────────────────────────────────────────────┐ ││
│  │   │ 预览/结果                                         │ ││
│  │   └───────────────────────────────────────────────────┘ ││
│  │                                                         ││
│  │   [预览] [执行] [撤销]                                  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  状态: 就绪                                                 │
└─────────────────────────────────────────────────────────────┘
```

### 快捷键

| 快捷键 | 操作 |
|--------|------|
| `Ctrl+Q` / `Cmd+Q` | 退出程序 |
| `Ctrl+Tab` | 切换到下一个工具 |
| `Ctrl+Shift+Tab` | 切换到上一个工具 |
| `Enter` | 执行当前操作 |
| `Esc` | 取消/清除选择 |

### 通用工作流程

1. **选择工具：** 点击侧边栏中的工具图标
2. **配置选项：** 在选项面板设置参数
3. **预览效果：** 点击"预览"查看预期结果
4. **执行操作：** 点击"执行"应用变更
5. **撤销操作：** 如需撤销，使用"撤销"按钮

---

## 工具详情

### 📝 SmartRename - 批量重命名

**功能：** 使用多种模式批量重命名文件

**支持模式：**

| 模式 | 说明 | 示例 |
|------|------|------|
| `sequence` | 序列编号 | file001.jpg, file002.jpg, file003.jpg |
| `date` | 日期前缀 | 2024-01-15_photo.jpg |
| `replace` | 查找替换 | 将"photo"替换为"img" |
| `lowercase` | 转小写 | PHOTO.JPG → photo.jpg |
| `uppercase` | 转大写 | photo.jpg → PHOTO.JPG |
| `clean` | 清理特殊字符 | 去除空格、括号等 |

**使用步骤：**
1. 选择目录（点击Browse或拖拽文件夹）
2. 选择重命名模式
3. 设置参数（起始编号、位数、查找替换文本）
4. 点击预览查看效果
5. 点击执行完成重命名

**撤销功能：** 执行后可点击"Undo Last"撤销最近操作

---

### 🖼️ ImgCrush - 图片压缩

**功能：** 批量压缩图片并转换HEIC格式

**操作类型：**

| 操作 | 说明 |
|------|------|
| Compress | 压缩图片减小文件大小 |
| Convert HEIC to JPG | iPhone照片格式转换 |

**参数说明：**

| 参数 | 范围 | 说明 |
|------|------|------|
| Quality | 10-100% | 压缩质量，数值越低文件越小但画质下降 |
| Max Width | 0-4000px | 最大宽度，超出将缩放；0表示不限制 |

**建议设置：**
- 网页图片：质量70%，最大宽度1920px
- 存档图片：质量85%，不限制宽度
- 预览图片：质量50%，最大宽度800px

---

### 📋 ClipStack - 剪贴板历史

**功能：** 自动记录剪贴板内容，支持搜索和整理

**界面说明：**

| 区域 | 功能 |
|------|------|
| Daemon Status | 后台守护进程状态 |
| Search Bar | 搜索历史内容 |
| Type Filter | 按类型过滤 |
| History Table | 剪贴板历史列表 |
| Action Buttons | 复制、固定、删除 |

**类型识别：**
- URL：网址链接
- Code：代码片段（含关键字识别）
- Text：普通文本

**守护进程：**
- 启动后台监控：点击"Start"
- 停止监控：点击"Stop"
- 自动记录复制内容到数据库

---

### 🌳 DirSnap - 目录快照

**功能：** 生成目录结构快照，多格式输出

**输出格式：**

| 格式 | 用途 |
|------|------|
| Tree | ASCII树形图，适合终端查看 |
| Markdown | Markdown列表，适合文档 |
| JSON | 结构化数据，适合程序处理 |
| HTML | 交互式网页，适合分享 |

**排除设置：**
常用排除目录：`node_modules, .git, __pycache__, dist, build`

---

### 🔐 EnvGuard - 环境变量备份

**功能：** 安全备份.env文件，AES-256加密

**安全特性：**
- AES-256-GCM加密算法
- 主密码保护
- 本地存储，不上传网络
- 支持云同步（iCloud/OneDrive/Dropbox）

**使用步骤：**
1. 设置主密码并解锁
2. 添加.env文件或扫描目录
3. 查看备份条目
4. 需要时获取并解密

---

## 故障排除

### 应用无法启动

```bash
# 检查Python版本
python3 --version  # 需要3.9+

# 验证PySide6
python3 -c "import PySide6; print('OK')"

# 如有问题，重新安装
pip install --force-reinstall PySide6
```

### macOS权限问题

```bash
# 允许执行权限
chmod +x install.py

# 移除隔离属性
xattr -cr .

# 首次运行从终端启动
open -a "macOS Tools Bundle"
```

### Windows Visual C++错误

下载安装：[Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Linux缺少依赖

```bash
# Ubuntu/Debian
sudo apt-get install libxcb-xinerama0 libxcb-cursor0

# Fedora
sudo dnf install libxcb-xinerama
```

### 预览显示空列表

- 确认已选择正确的目录
- 检查文件过滤条件是否过于严格
- 确认递归选项是否符合预期

---

## 开发

### 项目结构

```
macos-tools-gui/
├── gui/                     # GUI源码
│   ├── main.py              # 入口
│   ├── main_window.py       # 主窗口
│   ├── panels/              # 工具面板
│   ├── widgets/             # 自定义控件
│   ├── styles/              # 主题样式
│   └── resources/           # 资源文件
├── tests/                   # 测试
├── install.py               # 智能安装器
├── pyproject.toml           # 包配置
├── macos_tools_gui.spec     # PyInstaller配置
└── .github/workflows/       # CI/CD
```

### 本地构建

```bash
# 安装构建依赖
pip install pyinstaller pillow

# 构建
pyinstaller macos_tools_gui.spec --clean --noconfirm

# macOS产物: dist/macOS Tools Bundle.app
# Windows产物: dist/macOS Tools Bundle/
# Linux产物: dist/macOS Tools Bundle/
```

---

## 许可证

MIT 许可证 - 免费使用、修改和分发。

---

**[macOS 工具集](https://github.com/Francisezhang/macos-tools-bundle)的一部分**