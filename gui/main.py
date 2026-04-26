"""Main entry point for macOS Tools Bundle GUI."""

import sys
import platform
from pathlib import Path

# Add parent directory to path for CLI tools access
_bundle_path = Path(__file__).parent.parent.parent
if _bundle_path not in sys.path:
    sys.path.insert(0, str(_bundle_path))

from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont

from gui.main_window import MainWindow
from gui.styles.dark_theme import apply_dark_theme


def check_environment():
    """Check runtime environment and dependencies."""
    issues = []

    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        issues.append(f"Python 3.9+ required, found {version.major}.{version.minor}")

    # Check PySide6
    try:
        from PySide6.QtWidgets import QWidget
    except ImportError:
        issues.append("PySide6 not installed. Run: pip install PySide6")

    # Check platform support
    system = platform.system()
    if system not in ["Darwin", "Windows", "Linux"]:
        issues.append(f"Unsupported platform: {system}")

    return issues


def create_splash_screen():
    """Create a splash screen for startup."""
    # Create a simple splash pixmap
    pixmap = QPixmap(400, 200)
    pixmap.fill(QColor(45, 45, 45))

    painter = QPainter(pixmap)
    painter.setPen(QColor(255, 255, 255))
    painter.setFont(QFont("Arial", 24, QFont.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "🛠️ macOS Tools Bundle")

    painter.setFont(QFont("Arial", 12))
    painter.setPen(QColor(150, 150, 150))
    painter.drawText(0, 150, 400, 30, Qt.AlignCenter, "Loading...")

    painter.end()

    return QSplashScreen(pixmap)


def show_environment_error(issues: list):
    """Show environment check error dialog."""
    app = QApplication(sys.argv)

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Environment Error")
    msg.setText("Cannot start macOS Tools Bundle GUI")
    msg.setInformativeText("The following issues were detected:")
    msg.setDetailedText("\n".join(issues))
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #2d2d2d;
            color: #ffffff;
        }
        QLabel {
            color: #ffffff;
        }
        QPushButton {
            background-color: #0078d4;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1084d8;
        }
    """)
    msg.exec()

    sys.exit(1)


def main():
    """Launch the GUI application."""
    # Check environment first
    issues = check_environment()
    if issues:
        show_environment_error(issues)
        return

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

    # Show splash screen
    splash = create_splash_screen()
    splash.show()
    app.processEvents()

    # Create main window
    window = MainWindow()

    # Close splash and show window after a short delay
    QTimer.singleShot(500, lambda: (splash.finish(window), window.show()))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()