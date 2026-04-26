#!/usr/bin/env python3
"""
Local test runner for macOS Tools Bundle GUI.
Runs all checks before launching the application.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Run a command and report result."""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"⚠️ {result.stderr}")

    success = result.returncode == 0
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status}")

    return success


def main():
    """Run all local tests."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        🧪 macOS Tools Bundle GUI - Local Test Runner         ║
╚══════════════════════════════════════════════════════════════╝
""")

    all_passed = True

    # 1. Python version check
    version = sys.version_info
    print(f"\n🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required")
        all_passed = False
    else:
        print("✅ Python version OK")

    # 2. PySide6 check
    if not run_command(
        "python3 -c \"import PySide6.QtWidgets; print('PySide6 OK')\"",
        "Check PySide6 installation"
    ):
        all_passed = False

    # 3. GUI package import
    if not run_command(
        "python3 -c \"import sys; sys.path.insert(0, '.'); from gui.main_window import MainWindow; print('GUI import OK')\"",
        "Check GUI package import"
    ):
        all_passed = False

    # 4. Panel imports
    panels = [
        ("smartrename_panel", "SmartRename"),
        ("imgcrush_panel", "ImgCrush"),
        ("clipstack_panel", "ClipStack"),
        ("dirsnap_panel", "DirSnap"),
        ("envguard_panel", "EnvGuard"),
    ]

    print(f"\n{'='*60}")
    print("📋 Check Panel Imports")
    print(f"{'='*60}")

    for panel_file, panel_name in panels:
        try:
            result = subprocess.run(
                f"python3 -c \"import sys; sys.path.insert(0, '.'); from gui.panels.{panel_file} import *; print('{panel_name} OK')\"",
                shell=True, capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"  ✅ {panel_name}")
            else:
                print(f"  ⚠️ {panel_name} - CLI backend may be missing")
        except Exception as e:
            print(f"  ❌ {panel_name} - {str(e)[:30]}")

    # 5. Run pytest
    test_dir = Path("tests")
    if test_dir.exists():
        if not run_command("python3 -m pytest tests/ -v --tb=short", "Run unit tests"):
            all_passed = False
    else:
        print("\n⚠️ No tests directory found")

    # 6. Summary
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ All checks passed! Ready to run GUI.")
        print(f"{'='*60}")
        print("\nRun with: python3 -m gui.main")

        # Offer to launch
        response = input("\n🚀 Launch GUI now? [y/N]: ")
        if response.lower() == 'y':
            subprocess.run("python3 -m gui.main", shell=True)
    else:
        print("❌ Some checks failed. Fix issues before running.")
        print(f"{'='*60}")
        print("\nTry: python3 install.py")


if __name__ == "__main__":
    main()