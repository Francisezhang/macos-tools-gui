# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for macOS Tools Bundle GUI.

Build commands:
    pyinstaller macos_tools_gui.spec --clean

Output:
    dist/macOS Tools Bundle.app (macOS)
    dist/macOS Tools Bundle.exe (Windows)
"""

import sys
from pathlib import Path

block_cipher = None

# Determine bundle path
bundle_path = Path(SPECPATH).parent

a = Analysis(
    ['gui/main.py'],
    pathex=[str(bundle_path)],
    binaries=[],
    datas=[
        # Include CLI tool modules
        ('smartrename', 'smartrename'),
        ('imgcrush', 'imgcrush'),
        ('clipstack', 'clipstack'),
        ('dirsnap', 'dirsnap'),
        ('envguard', 'envguard'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'smartrename',
        'smartrename.core',
        'smartrename.core.renamer',
        'smartrename.core.patterns',
        'smartrename.core.undo',
        'imgcrush',
        'imgcrush.core',
        'imgcrush.core.compressor',
        'imgcrush.core.converter',
        'clipstack',
        'clipstack.core',
        'clipstack.core.storage',
        'clipstack.core.search',
        'clipstack.core.monitor',
        'dirsnap',
        'dirsnap.core',
        'dirsnap.core.scanner',
        'dirsnap.core.renderer',
        'envguard',
        'envguard.core',
        'envguard.core.vault',
        'envguard.core.crypto',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='macOS Tools Bundle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI mode, no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icons/app.ico' if sys.platform == 'win32' else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='macOS Tools Bundle',
)

# macOS app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='macOS Tools Bundle.app',
        icon='resources/icons/app.icns',
        bundle_identifier='com.francisezhang.macos-tools',
        version='1.0.0',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleLongVersionString': '1.0.0',
            'NSHumanReadableCopyright': 'Copyright © 2026 Francisezhang. MIT License.',
        },
    )