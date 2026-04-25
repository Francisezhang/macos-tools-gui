"""Main entry point for macOS Tools Bundle GUI."""

import sys
from pathlib import Path

# Add parent directory to path for CLI tools access
_bundle_path = Path(__file__).parent.parent.parent
if _bundle_path not in sys.path:
    sys.path.insert(0, str(_bundle_path))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from gui.main_window import MainWindow
from gui.styles.dark_theme import apply_dark_theme


def main():
    """Launch the GUI application."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("macOS Tools Bundle")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Francisezhang")

    # Apply dark theme
    apply_dark_theme(app)

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()