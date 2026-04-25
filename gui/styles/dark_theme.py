"""Dark theme styling for the application."""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette


DARK_COLORS = {
    "window": "#1e1e1e",
    "window_text": "#ffffff",
    "base": "#2d2d2d",
    "alternate_base": "#3d3d3d",
    "tooltip_base": "#2d2d2d",
    "tooltip_text": "#ffffff",
    "text": "#ffffff",
    "button": "#3d3d3d",
    "button_text": "#ffffff",
    "bright_text": "#ffffff",
    "link": "#0078d4",
    "highlight": "#0078d4",
    "highlighted_text": "#ffffff",
    "disabled_text": "#666666",
}


def apply_dark_theme(app: QApplication):
    """Apply dark theme to the application."""
    palette = QPalette()

    palette.setColor(QPalette.Window, QColor(DARK_COLORS["window"]))
    palette.setColor(QPalette.WindowText, QColor(DARK_COLORS["window_text"]))
    palette.setColor(QPalette.Base, QColor(DARK_COLORS["base"]))
    palette.setColor(QPalette.AlternateBase, QColor(DARK_COLORS["alternate_base"]))
    palette.setColor(QPalette.ToolTipBase, QColor(DARK_COLORS["tooltip_base"]))
    palette.setColor(QPalette.ToolTipText, QColor(DARK_COLORS["tooltip_text"]))
    palette.setColor(QPalette.Text, QColor(DARK_COLORS["text"]))
    palette.setColor(QPalette.Button, QColor(DARK_COLORS["button"]))
    palette.setColor(QPalette.ButtonText, QColor(DARK_COLORS["button_text"]))
    palette.setColor(QPalette.BrightText, QColor(DARK_COLORS["bright_text"]))
    palette.setColor(QPalette.Link, QColor(DARK_COLORS["link"]))
    palette.setColor(QPalette.Highlight, QColor(DARK_COLORS["highlight"]))
    palette.setColor(QPalette.HighlightedText, QColor(DARK_COLORS["highlighted_text"]))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(DARK_COLORS["disabled_text"]))

    app.setPalette(palette)

    # Additional stylesheet for common widgets
    app.setStyleSheet("""
        QToolTip {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #4d4d4d;
            padding: 5px;
        }

        QScrollBar:vertical {
            background-color: #2d2d2d;
            width: 12px;
        }

        QScrollBar::handle:vertical {
            background-color: #4d4d4d;
            min-height: 20px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #5d5d5d;
        }

        QScrollBar:horizontal {
            background-color: #2d2d2d;
            height: 12px;
        }

        QScrollBar::handle:horizontal {
            background-color: #4d4d4d;
            min-width: 20px;
            border-radius: 6px;
        }

        QProgressBar {
            background-color: #2d2d2d;
            border: none;
            border-radius: 4px;
            text-align: center;
            color: #ffffff;
        }

        QProgressBar::chunk {
            background-color: #0078d4;
            border-radius: 4px;
        }

        QComboBox {
            background-color: #3d3d3d;
            color: #ffffff;
            border: 1px solid #4d4d4d;
            border-radius: 4px;
            padding: 5px;
        }

        QComboBox:hover {
            border: 1px solid #5d5d5d;
        }

        QComboBox::drop-down {
            border: none;
            width: 20px;
        }

        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #ffffff;
        }

        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            color: #ffffff;
            selection-background-color: #0078d4;
        }

        QSlider::groove:horizontal {
            background-color: #3d3d3d;
            height: 6px;
            border-radius: 3px;
        }

        QSlider::handle:horizontal {
            background-color: #0078d4;
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }

        QSlider::handle:horizontal:hover {
            background-color: #1a8cdb;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }

        QCheckBox::indicator:unchecked {
            background-color: #3d3d3d;
            border: 1px solid #4d4d4d;
            border-radius: 3px;
        }

        QCheckBox::indicator:checked {
            background-color: #0078d4;
            border: 1px solid #0078d4;
            border-radius: 3px;
        }
    """)