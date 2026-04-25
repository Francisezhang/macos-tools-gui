"""Base panel class for tool panels."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class BasePanel(QWidget):
    """Base class for all tool panels."""

    tool_name: str = "Unknown"
    tool_icon: str = "❓"
    tool_description: str = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_header()
        self._setup_content()

    def _setup_header(self):
        """Setup panel header with title and description."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Header layout
        header_layout = QHBoxLayout()

        # Icon
        icon_label = QLabel(self.tool_icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 32))
        icon_label.setStyleSheet("color: #ffffff;")
        header_layout.addWidget(icon_label)

        # Title and description
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)

        title_label = QLabel(self.tool_name)
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        title_layout.addWidget(title_label)

        if self.tool_description:
            desc_label = QLabel(self.tool_description)
            desc_label.setFont(QFont("Segoe UI", 12))
            desc_label.setStyleSheet("color: #888888;")
            title_layout.addWidget(desc_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        self.main_layout.addLayout(header_layout)

        # Separator line
        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #3d3d3d;")
        self.main_layout.addWidget(separator)

    def _setup_content(self):
        """Setup panel content area. Override in subclasses."""
        # Placeholder content
        placeholder = QLabel("Panel content will be implemented here")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("color: #666666;")
        self.main_layout.addWidget(placeholder)

    def add_button(self, text: str, callback=None, primary: bool = False) -> QPushButton:
        """Add a styled button to the panel."""
        btn = QPushButton(text)
        btn.setFixedHeight(36)
        btn.setCursor(Qt.PointingHandCursor)

        if primary:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    color: #ffffff;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1a8cdb;
                }
                QPushButton:pressed {
                    background-color: #006cbd;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #4d4d4d;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                    border: 1px solid #5d5d5d;
                }
                QPushButton:pressed {
                    background-color: #5d5d5d;
                }
            """)

        if callback:
            btn.clicked.connect(callback)

        return btn