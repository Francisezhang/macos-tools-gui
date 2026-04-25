"""ImgCrush GUI panel."""

from pathlib import Path
from typing import List
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSlider, QCheckBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog,
    QGroupBox, QWidget, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor

# Import CLI backend
import sys
_bundle_path = Path(__file__).parent.parent.parent.parent.parent
imgcrush_path = _bundle_path / "imgcrush"
if imgcrush_path not in sys.path:
    sys.path.insert(0, str(imgcrush_path))

try:
    from imgcrush.core.compressor import compress_directory, estimate_compressed_size
    from imgcrush.core.converter import convert_directory
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False

from gui.widgets.base_panel import BasePanel


class CompressWorker(QThread):
    """Background thread for compression."""
    progress = Signal(int)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, directory: Path, quality: int, max_width: int, pattern: str):
        super().__init__()
        self.directory = directory
        self.quality = quality
        self.max_width = max_width
        self.pattern = pattern

    def run(self):
        if not CLI_AVAILABLE:
            self.error.emit("CLI backend not available")
            return

        try:
            result = compress_directory(
                self.directory,
                quality=self.quality,
                max_width=self.max_width,
                pattern=self.pattern,
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ImgCrushPanel(BasePanel):
    """GUI panel for ImgCrush tool."""

    tool_name = "ImgCrush"
    tool_icon = "🖼️"
    tool_description = "Batch image compression and HEIC to JPG conversion"

    def __init__(self, parent=None):
        self.selected_directory = None
        self.image_files = []
        super().__init__(parent)

    def _setup_content(self):
        """Setup panel content."""
        # Directory selection
        dir_group = QGroupBox("Directory")
        dir_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
            }
        """)
        dir_layout = QHBoxLayout(dir_group)

        self.dir_label = QLabel("No directory selected")
        self.dir_label.setStyleSheet("color: #888888;")
        dir_layout.addWidget(self.dir_label, stretch=1)

        self.browse_btn = self.add_button("Browse...", self._browse_directory)
        dir_layout.addWidget(self.browse_btn)

        self.main_layout.addWidget(dir_group)

        # Operation selection
        op_group = QGroupBox("Operation")
        op_group.setStyleSheet(dir_group.styleSheet())
        op_layout = QVBoxLayout(op_group)

        op_row = QHBoxLayout()
        op_label = QLabel("Operation:")
        op_label.setStyleSheet("color: #ffffff;")
        op_row.addWidget(op_label)

        self.op_combo = QComboBox()
        self.op_combo.addItems(["Compress", "Convert HEIC to JPG"])
        self.op_combo.currentTextChanged.connect(self._on_operation_changed)
        op_row.addWidget(self.op_combo)
        op_row.addStretch()
        op_layout.addLayout(op_row)

        self.main_layout.addWidget(op_group)

        # Compress options
        self.compress_group = QGroupBox("Compression Options")
        self.compress_group.setStyleSheet(dir_group.styleSheet())
        compress_layout = QVBoxLayout(self.compress_group)

        # Quality slider
        quality_row = QHBoxLayout()
        quality_label = QLabel("Quality:")
        quality_label.setStyleSheet("color: #ffffff;")
        quality_row.addWidget(quality_label)

        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(10, 100)
        self.quality_slider.setValue(70)
        self.quality_slider.setTickPosition(QSlider.TicksBelow)
        self.quality_slider.setTickInterval(10)
        self.quality_slider.valueChanged.connect(self._update_quality_label)
        quality_row.addWidget(self.quality_slider)

        self.quality_value_label = QLabel("70%")
        self.quality_value_label.setStyleSheet("color: #0078d4;")
        quality_row.addWidget(self.quality_value_label)
        quality_row.addStretch()
        compress_layout.addLayout(quality_row)

        # Max width
        width_row = QHBoxLayout()
        width_label = QLabel("Max width (optional):")
        width_label.setStyleSheet("color: #ffffff;")
        width_row.addWidget(width_label)

        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(0, 4000)
        self.width_slider.setValue(0)
        self.width_slider.setTickPosition(QSlider.TicksBelow)
        self.width_slider.setTickInterval(500)
        self.width_slider.valueChanged.connect(self._update_width_label)
        width_row.addWidget(self.width_slider)

        self.width_value_label = QLabel("No limit")
        self.width_value_label.setStyleSheet("color: #888888;")
        width_row.addWidget(self.width_value_label)
        width_row.addStretch()
        compress_layout.addLayout(width_row)

        # Pattern filter
        pattern_row = QHBoxLayout()
        pattern_label = QLabel("Filter:")
        pattern_label.setStyleSheet("color: #ffffff;")
        pattern_row.addWidget(pattern_label)

        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("*.jpg (optional)")
        self.pattern_input.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        pattern_row.addWidget(self.pattern_input)
        pattern_row.addStretch()
        compress_layout.addLayout(pattern_row)

        self.main_layout.addWidget(self.compress_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
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
        """)
        self.main_layout.addWidget(self.progress_bar)

        # Results table
        results_group = QGroupBox("Results")
        results_group.setStyleSheet(dir_group.styleSheet())
        results_layout = QVBoxLayout(results_group)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["File", "Original Size", "New Size"])
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                gridline-color: #3d3d3d;
            }
            QHeaderView::section {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                padding: 5px;
            }
        """)
        results_layout.addWidget(self.results_table)

        self.savings_label = QLabel("Total savings: 0 KB")
        self.savings_label.setStyleSheet("color: #888888;")
        results_layout.addWidget(self.savings_label)

        self.main_layout.addWidget(results_group)

        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.execute_btn = self.add_button("Execute", self._execute_operation, primary=True)
        action_layout.addWidget(self.execute_btn)

        self.main_layout.addLayout(action_layout)

    def _on_operation_changed(self, operation: str):
        """Handle operation change."""
        if operation == "Convert HEIC to JPG":
            self.compress_group.hide()
        else:
            self.compress_group.show()

    def _update_quality_label(self, value: int):
        """Update quality label."""
        self.quality_value_label.setText(f"{value}%")

    def _update_width_label(self, value: int):
        """Update width label."""
        if value == 0:
            self.width_value_label.setText("No limit")
            self.width_value_label.setStyleSheet("color: #888888;")
        else:
            self.width_value_label.setText(f"{value}px")
            self.width_value_label.setStyleSheet("color: #0078d4;")

    def _browse_directory(self):
        """Browse for directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory with Images",
            "",
            QFileDialog.ShowDirsOnly
        )

        if directory:
            self.selected_directory = Path(directory)
            self.dir_label.setText(str(self.selected_directory))
            self.dir_label.setStyleSheet("color: #ffffff;")

    def _execute_operation(self):
        """Execute the selected operation."""
        if not self.selected_directory:
            QMessageBox.warning(self, "No Directory", "Please select a directory first.")
            return

        if not CLI_AVAILABLE:
            QMessageBox.warning(
                self,
                "CLI Not Available",
                "ImgCrush CLI backend is not installed.\nPlease install: pip install imgcrush"
            )
            return

        operation = self.op_combo.currentText()

        if operation == "Compress":
            quality = self.quality_slider.value()
            max_width = self.width_slider.value() if self.width_slider.value() > 0 else None
            pattern = self.pattern_input.text() or None

            self.compress_worker = CompressWorker(
                self.selected_directory,
                quality,
                max_width,
                pattern
            )
            self.compress_worker.finished.connect(self._display_results)
            self.compress_worker.error.connect(self._on_compress_error)
            self.compress_worker.start()

            self.progress_bar.setValue(0)
            self.execute_btn.setEnabled(False)
            self.execute_btn.setText("Processing...")

        elif operation == "Convert HEIC to JPG":
            try:
                result = convert_directory(
                    self.selected_directory,
                    target_format="jpg",
                    pattern="*.heic"
                )
                self._display_results(result)
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _on_compress_error(self, error_msg: str):
        """Handle compression error."""
        self.execute_btn.setEnabled(True)
        self.execute_btn.setText("Execute")
        self.progress_bar.setValue(0)
        QMessageBox.warning(self, "Compression Error", error_msg)

    def _display_results(self, result: dict):
        """Display compression results."""
        self.execute_btn.setEnabled(True)
        self.execute_btn.setText("Execute")
        self.progress_bar.setValue(100)

        if not result.get("success"):
            QMessageBox.warning(self, "Error", result.get("error", "Unknown error"))
            return

        files = result.get("files", [])
        self.results_table.setRowCount(len(files))

        total_original = 0
        total_compressed = 0

        for row, file_info in enumerate(files):
            name_item = QTableWidgetItem(file_info.get("name", "Unknown"))

            orig_size = file_info.get("original_size", 0)
            orig_item = QTableWidgetItem(f"{orig_size / 1024:.1f} KB")
            total_original += orig_size

            comp_size = file_info.get("compressed_size", orig_size)
            comp_item = QTableWidgetItem(f"{comp_size / 1024:.1f} KB")
            total_compressed += comp_size

            if comp_size < orig_size:
                comp_item.setForeground(QColor("#00d400"))

            self.results_table.setItem(row, 0, name_item)
            self.results_table.setItem(row, 1, orig_item)
            self.results_table.setItem(row, 2, comp_item)

        savings = total_original - total_compressed
        if savings > 0:
            self.savings_label.setText(f"Total savings: {savings / 1024:.1f} KB ({savings / total_original * 100:.1f}%)")
            self.savings_label.setStyleSheet("color: #00d400;")
        else:
            self.savings_label.setText(f"No savings")
            self.savings_label.setStyleSheet("color: #888888;")