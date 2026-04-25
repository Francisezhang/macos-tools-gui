# macOS 工具集 GUI

**5款CLI工具的跨平台图形界面**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)

## 概述

此GUI为macOS工具集CLI工具提供统一启动器，让偏好图形界面的用户也能使用这些工具。

**包含工具：**
- 📝 **SmartRename** — 批量文件重命名（6种模式）
- 🖼️ **ImgCrush** — 图片压缩和HEIC转换
- 📋 **ClipStack** — 剪贴板历史管理
- 🌳 **DirSnap** — 目录结构快照
- 🔐 **EnvGuard** — 加密.env备份

## 安装

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/Francisezhang/macos-tools-bundle
cd macos-tools-bundle/gui

# 安装依赖
pip install -e .

# 运行
python -m gui.main
```

### 预编译包

| 平台 | 格式 | 下载 |
|------|------|------|
| macOS | .app 包 | [Releases](https://github.com/Francisezhang/macos-tools-bundle/releases) |
| Windows | .exe 安装程序 | [Releases](https://github.com/Francisezhang/macos-tools-bundle/releases) |
| Linux | .deb 包 | [Releases](https://github.com/Francisezhang/macos-tools-bundle/releases) |

## 特性

- **深色主题**: 现代深色UI设计
- **拖拽支持**: 直接拖放文件到面板
- **实时预览**: 执行前查看变更
- **进度指示**: 操作时可视化反馈
- **跨平台**: macOS/Windows/Linux相同界面

## 开发

```bash
# 本地构建
pyinstaller macos_tools_gui.spec --clean
```

## 许可证

MIT 许可证 — 免费使用、修改和分发。

---

**[macOS 工具集](https://github.com/Francisezhang/macos-tools-bundle)的一部分**