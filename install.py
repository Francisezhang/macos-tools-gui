#!/usr/bin/env python3
"""
macOS Tools Bundle GUI - Smart Installer
自动检测运行环境并安装必要依赖

支持平台: macOS, Windows, Linux
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


class Colors:
    """终端颜色"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header():
    """打印安装器标题"""
    print(f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║     🛠️  macOS Tools Bundle GUI - Smart Installer v1.0       ║
║                                                              ║
║     Cross-platform GUI for 5 productivity tools              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")


def print_step(step: str, message: str):
    """打印步骤信息"""
    print(f"{Colors.BLUE}[{step}]{Colors.END} {message}")


def print_success(message: str):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message: str):
    """打印错误信息"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_warning(message: str):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def detect_platform():
    """检测运行平台"""
    system = platform.system()
    version = platform.version()
    machine = platform.machine()

    print_step("DETECT", f"Platform: {system} ({machine})")
    print_step("DETECT", f"Version: {version}")

    return {
        "system": system,
        "version": version,
        "machine": machine,
        "is_macos": system == "Darwin",
        "is_windows": system == "Windows",
        "is_linux": system == "Linux",
        "is_arm": machine in ["arm64", "aarch64"],
        "is_x86": machine in ["x86_64", "AMD64", "x86"],
    }


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    print_step("CHECK", f"Python version: {version_str}")

    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_error(f"Python 3.9+ required, found {version_str}")
        print_warning("Please upgrade Python: https://python.org/downloads/")
        return False

    print_success(f"Python {version_str} meets requirements (3.9+)")
    return True


def check_pip():
    """检查pip是否可用"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print_success(f"pip available: {result.stdout.strip()}")
            return True
    except Exception:
        pass

    print_error("pip not available")
    print_warning("Try: python -m ensurepip")
    return False


def install_dependencies():
    """安装必要的依赖"""
    dependencies = [
        ("PySide6", "PySide6>=6.6.0", "Qt GUI framework"),
        ("Pillow", "Pillow>=9.0.0", "Image processing (optional)"),
    ]

    print_step("INSTALL", "Installing dependencies...")

    for name, spec, desc in dependencies:
        print(f"  {Colors.CYAN}• {name}{Colors.END} - {desc}")

        try:
            # 先检查是否已安装
            result = subprocess.run(
                [sys.executable, "-c", f"import {name}; print({name}.__version__)"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                print_success(f"{name} already installed (v{version})")
                continue

        except Exception:
            pass

        # 安装依赖
        print(f"  {Colors.YELLOW}Installing {name}...{Colors.END}")

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", spec],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print_success(f"{name} installed successfully")
            else:
                print_error(f"Failed to install {name}")
                print_warning(result.stderr[:200] if result.stderr else "Unknown error")
                return False

        except subprocess.TimeoutExpired:
            print_error(f"Timeout installing {name}")
            return False
        except Exception as e:
            print_error(f"Error installing {name}: {str(e)[:50]}")
            return False

    return True


def verify_installation():
    """验证安装"""
    print_step("VERIFY", "Verifying installation...")

    # 检查核心模块
    modules = [
        ("PySide6.QtWidgets", "GUI framework"),
        ("PySide6.QtCore", "Qt core"),
        ("PySide6.QtGui", "Qt GUI"),
    ]

    for module, desc in modules:
        try:
            result = subprocess.run(
                [sys.executable, "-c", f"import {module}; print('OK')"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and "OK" in result.stdout:
                print_success(f"{module} - {desc}")
            else:
                print_error(f"{module} import failed")
                return False

        except Exception as e:
            print_error(f"{module}: {str(e)[:30]}")
            return False

    return True


def check_gui_package():
    """检查GUI包是否可导入"""
    print_step("CHECK", "Checking GUI package...")

    # 获取当前目录
    script_dir = Path(__file__).parent.absolute()

    try:
        # 添加路径并测试导入
        result = subprocess.run(
            [sys.executable, "-c", f"""
import sys
sys.path.insert(0, '{script_dir}')
from gui.main_window import MainWindow
print('GUI import OK')
"""],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and "OK" in result.stdout:
            print_success("GUI package imports successfully")
            return True
        else:
            print_warning("GUI package not found or import failed")
            print_warning("Run from the gui directory or install the package")
            return False

    except Exception as e:
        print_warning(f"GUI check: {str(e)[:50]}")
        return False


def create_desktop_shortcut(platform_info: dict):
    """创建桌面快捷方式"""
    script_dir = Path(__file__).parent.absolute()

    if platform_info["is_macos"]:
        # macOS: 创建 .app wrapper
        app_dir = Path.home() / "Applications" / "macOS Tools Bundle.app"
        if not app_dir.exists():
            print_step("SHORTCUT", "Creating macOS app shortcut...")
            try:
                app_dir.mkdir(parents=True, exist_ok=True)
                contents_dir = app_dir / "Contents"
                contents_dir.mkdir(exist_ok=True)
                macos_dir = contents_dir / "MacOS"
                macos_dir.mkdir(exist_ok=True)

                # 创建启动脚本
                launcher = macos_dir / "macOS Tools Bundle"
                launcher.write_text(f'''#!/bin/bash
cd "{script_dir}"
python3 -m gui.main
''')
                launcher.chmod(0o755)

                # 创建 Info.plist
                info_plist = contents_dir / "Info.plist"
                info_plist.write_text('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>macOS Tools Bundle</string>
    <key>CFBundleDisplayName</key>
    <string>macOS Tools Bundle</string>
    <key>CFBundleIdentifier</key>
    <string>com.francisezhang.macos-tools</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>''')

                print_success(f"Shortcut created: {app_dir}")
            except Exception as e:
                print_warning(f"Could not create shortcut: {str(e)[:50]}")

    elif platform_info["is_windows"]:
        # Windows: 创建 .bat 启动器
        print_step("SHORTCUT", "Creating Windows launcher...")
        bat_file = script_dir / "launch_gui.bat"
        bat_file.write_text(f'''@echo off
cd /d "{script_dir}"
python -m gui.main
pause
''')
        print_success(f"Launcher created: {bat_file}")

    elif platform_info["is_linux"]:
        # Linux: 创建桌面文件
        print_step("SHORTCUT", "Creating Linux desktop entry...")
        desktop_file = Path.home() / ".local" / "share" / "applications" / "macos-tools-gui.desktop"
        desktop_file.parent.mkdir(parents=True, exist_ok=True)
        desktop_file.write_text(f'''[Desktop Entry]
Name=macOS Tools Bundle
Comment=Cross-platform GUI for productivity tools
Exec=python3 -m gui.main
Path={script_dir}
Icon=applications-other
Terminal=false
Type=Application
Categories=Utility;
''')
        desktop_file.chmod(0o755)
        print_success(f"Desktop entry created: {desktop_file}")


def print_usage():
    """打印使用说明"""
    print(f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════════
                    📖 使用说明 / Usage Guide
═══════════════════════════════════════════════════════════════════{Colors.END}

{Colors.BOLD}启动方式 / How to Launch:{Colors.END}

  {Colors.GREEN}方式1 - 命令行启动:{Colors.END}
    cd {Path(__file__).parent}
    python3 -m gui.main

  {Colors.GREEN}方式2 - 直接运行:{Colors.END}
    python3 gui/gui/main.py

  {Colors.GREEN}方式3 - 已安装包:{Colors.END}
    macos-tools-gui

{Colors.BOLD}工具说明 / Tool Overview:{Colors.END}

  📝 SmartRename - 批量文件重命名
     • 支持序列号、日期、替换、大小写转换
     • 预览功能，执行前查看变更
     • 支持撤销最近操作

  🖼️ ImgCrush - 图片压缩转换
     • 调整质量参数 (10-100%)
     • HEIC → JPG 转换
     • 实时显示压缩效果

  📋 ClipStack - 剪贴板历史
     • 自动记录复制内容
     • 搜索、固定、删除功能
     • 支持URL、代码识别

  🌳 DirSnap - 目录快照
     • 多格式输出 (Tree/Markdown/JSON/HTML)
     • 递归扫描，排除特定目录
     • 统计文件数量和大小

  🔐 EnvGuard - 环境变量备份
     • AES-256-GCM 加密
     • 搜索本地 .env 文件
     • 云同步支持 (iCloud/OneDrive)

{Colors.BOLD}快捷键 / Keyboard Shortcuts:{Colors.END}

  Ctrl+Q / Cmd+Q  - 退出程序
  Ctrl+S / Cmd+S  - 保存当前操作
  Ctrl+R / Cmd+R  - 刷新预览

{Colors.BOLD}故障排除 / Troubleshooting:{Colors.END}

  • 如果界面无法启动，检查 PySide6 是否正确安装
  • macOS: 如果提示权限问题，在终端运行 chmod +x
  • Windows: 确保安装了 Visual C++ Redistributable
  • Linux: 础保安装了 libxcb-xinerama0

{Colors.BOLD}获取帮助 / Get Help:{Colors.END}

  GitHub: https://github.com/Francisezhang/macos-tools-gui
  Issues: https://github.com/Francisezhang/macos-tools-gui/issues

""")


def main():
    """主安装流程"""
    print_header()

    # 1. 检测平台
    platform_info = detect_platform()

    # 2. 检查Python版本
    if not check_python_version():
        sys.exit(1)

    # 3. 检查pip
    if not check_pip():
        sys.exit(1)

    # 4. 安装依赖
    if not install_dependencies():
        print_error("Dependency installation failed")
        print_warning("Try manual install: pip install PySide6 Pillow")
        sys.exit(1)

    # 5. 验证安装
    if not verify_installation():
        print_error("Installation verification failed")
        sys.exit(1)

    # 6. 检查GUI包
    gui_ok = check_gui_package()

    # 7. 创建快捷方式（可选）
    try:
        create_desktop_shortcut(platform_info)
    except Exception:
        pass

    # 8. 打印使用说明
    print_usage()

    # 9. 完成提示
    print(f"""
{Colors.GREEN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║              ✓ 安装完成 / Installation Complete              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.CYAN}现在可以启动 GUI / Ready to launch:{Colors.END}
  {Colors.BOLD}python3 -m gui.main{Colors.END}

""")


if __name__ == "__main__":
    main()