"""Main window for macOS Tools Bundle GUI."""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon


class ToolButton(QPushButton):
    """Custom styled button for tool selection."""

    def __init__(self, icon_text: str, title: str, description: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.panel_class = None

        # Setup appearance
        self.setFixedSize(120, 100)
        self.setCursor(Qt.PointingHandCursor)

        # Create layout inside button
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Icon (emoji or text)
        icon_label = QLabel(icon_text)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        layout.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(title_label)


class PlaceholderPanel(QWidget):
    """Placeholder panel when CLI backend is not available."""

    def __init__(self, tool_name: str, tool_icon: str, cli_name: str):
        super().__init__()
        self.tool_name = tool_name
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Icon
        icon = QLabel(tool_icon)
        icon.setFont(QFont("Segoe UI Emoji", 48))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        # Title
        title = QLabel(tool_name)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #ffffff;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        # Warning message
        msg = QLabel(f"CLI backend ({cli_name}) is not installed or not found.\n\n"
                    f"To use this tool, install the CLI package:\n"
                    f"pip install {cli_name}\n\n"
                    f"Or run the GUI from the full bundle directory.")
        msg.setFont(QFont("Segoe UI", 12))
        msg.setStyleSheet("color: #888888;")
        msg.setAlignment(Qt.AlignCenter)
        layout.addWidget(msg)

        layout.addSpacing(20)

        # Install button
        install_btn = QPushButton(f"pip install {cli_name}")
        install_btn.setFixedSize(200, 40)
        install_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
        """)
        install_btn.clicked.connect(self._install_cli)
        layout.addWidget(install_btn)

        self.cli_name = cli_name

    def _install_cli(self):
        """Attempt to install CLI package."""
        import subprocess
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", self.cli_name],
                capture_output=True
            )
            QMessageBox.information(
                self,
                "Installation",
                f"Attempted to install {self.cli_name}.\n\n"
                "If successful, restart the application to use this tool."
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Installation failed: {str(e)}")


def create_panel_safe(panel_name: str) -> QWidget:
    """Safely create a panel, returning placeholder if import fails."""
    try:
        if panel_name == "smartrename":
            from gui.panels.smartrename_panel import SmartRenamePanel
            return SmartRenamePanel()
        elif panel_name == "imgcrush":
            from gui.panels.imgcrush_panel import ImgCrushPanel
            return ImgCrushPanel()
        elif panel_name == "clipstack":
            from gui.panels.clipstack_panel import ClipStackPanel
            return ClipStackPanel()
        elif panel_name == "dirsnap":
            from gui.panels.dirsnap_panel import DirSnapPanel
            return DirSnapPanel()
        elif panel_name == "envguard":
            from gui.panels.envguard_panel import EnvGuardPanel
            return EnvGuardPanel()
    except ImportError as e:
        # Return placeholder panel
        tool_info = {
            "smartrename": ("SmartRename", "📝", "smartrename"),
            "imgcrush": ("ImgCrush", "🖼️", "imgcrush"),
            "clipstack": ("ClipStack", "📋", "clipstack"),
            "dirsnap": ("DirSnap", "🌳", "dirsnap"),
            "envguard": ("EnvGuard", "🔐", "envguard"),
        }
        info = tool_info.get(panel_name, (panel_name, "❓", panel_name))
        return PlaceholderPanel(info[0], info[1], info[2])


class MainWindow(QMainWindow):
    """Main application window with tool launcher and panel container."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("macOS Tools Bundle")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup the main UI layout."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout: sidebar + content
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar (tool buttons)
        sidebar = QFrame()
        sidebar.setFixedWidth(140)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-right: 1px solid #3d3d3d;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(15)

        # Tool buttons
        self.tools = {
            "smartrename": ToolButton("📝", "Rename", "Batch file renaming"),
            "imgcrush": ToolButton("🖼️", "ImgCrush", "Image compression"),
            "clipstack": ToolButton("📋", "Clipboard", "History manager"),
            "dirsnap": ToolButton("🌳", "DirSnap", "Directory tree"),
            "envguard": ToolButton("🔐", "EnvGuard", ".env backup"),
        }

        for tool_id, button in self.tools.items():
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d3d;
                    border: 1px solid #4d4d4d;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                    border: 1px solid #5d5d5d;
                }
                QPushButton:checked {
                    background-color: #0078d4;
                    border: 1px solid #0078d4;
                }
            """)
            button.setCheckable(True)
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        # Settings button
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setFixedHeight(40)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888888;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
        sidebar_layout.addWidget(settings_btn)

        main_layout.addWidget(sidebar)

        # Content area (stacked panels)
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: #1e1e1e;
            }
        """)

        # Home panel (welcome screen)
        home_panel = self._create_home_panel()
        self.content_stack.addWidget(home_panel)

        # Tool panels (lazy load with error handling)
        self.panels = {}
        for tool_id in self.tools.keys():
            panel = create_panel_safe(tool_id)
            self.panels[tool_id] = panel
            self.content_stack.addWidget(panel)

        main_layout.addWidget(self.content_stack, stretch=1)

        # Select first tool
        self.tools["smartrename"].setChecked(True)

    def _create_home_panel(self) -> QWidget:
        """Create welcome/home panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("macOS Tools Bundle")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: #ffffff;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Cross-platform CLI tools with GUI interface\nmacOS • Windows • Linux")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #888888;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        # Description
        desc = QLabel("Select a tool from the sidebar to begin")
        desc.setFont(QFont("Segoe UI", 12))
        desc.setStyleSheet("color: #666666;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        layout.addSpacing(20)

        # Note about standalone mode
        note = QLabel("Note: Running in standalone mode.\nCLI backends may require separate installation.")
        note.setFont(QFont("Segoe UI", 10))
        note.setStyleSheet("color: #555555;")
        note.setAlignment(Qt.AlignCenter)
        layout.addWidget(note)

        return panel

    def _connect_signals(self):
        """Connect button signals."""
        for tool_id, button in self.tools.items():
            button.clicked.connect(self._on_tool_selected)

    def _on_tool_selected(self):
        """Handle tool button click."""
        # Uncheck all other buttons
        sender = self.sender()
        for tool_id, button in self.tools.items():
            if button != sender:
                button.setChecked(False)

        # Find which tool was selected
        for tool_id, button in self.tools.items():
            if button.isChecked():
                if tool_id in self.panels:
                    self.content_stack.setCurrentWidget(self.panels[tool_id])
                else:
                    self.content_stack.setCurrentIndex(0)  # Home
                break