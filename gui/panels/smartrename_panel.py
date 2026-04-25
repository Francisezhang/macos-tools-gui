"""SmartRename GUI panel."""

from pathlib import Path
from typing import List, Dict
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QCheckBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog,
    QGroupBox, QSpinBox, QWidget, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor

# Import CLI backend
import sys
_bundle_path = Path(__file__).parent.parent.parent.parent.parent
smartrename_path = _bundle_path / "smartrename"
if smartrename_path not in sys.path:
    sys.path.insert(0, str(smartrename_path))

try:
    from smartrename.core.renamer import collect_files, preview_rename, rename_directory
    from smartrename.core.patterns import get_pattern_func
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False

from gui.widgets.base_panel import BasePanel


class PreviewWorker(QThread):
    """Background thread for generating preview."""
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, directory: Path, mode: str, pattern: str, recursive: bool, **kwargs):
        super().__init__()
        self.directory = directory
        self.mode = mode
        self.pattern = pattern
        self.recursive = recursive
        self.kwargs = kwargs

    def run(self):
        if not CLI_AVAILABLE:
            self.error.emit("CLI backend not available")
            return

        try:
            files = collect_files(self.directory, self.pattern, self.recursive)
            pattern_func = get_pattern_func(self.mode, **self.kwargs)
            operations = preview_rename(files, self.mode, pattern_func, **self.kwargs)
            self.finished.emit(operations)
        except Exception as e:
            self.error.emit(str(e))


class SmartRenamePanel(BasePanel):
    """GUI panel for SmartRename tool."""

    tool_name = "SmartRename"
    tool_icon = "📝"
    tool_description = "Batch file renaming with 6 patterns and undo support"

    def __init__(self, parent=None):
        self.selected_directory = None
        self.preview_operations = []
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

        # Rename options
        options_group = QGroupBox("Rename Options")
        options_group.setStyleSheet(dir_group.styleSheet())
        options_layout = QVBoxLayout(options_group)

        # Mode selection
        mode_row = QHBoxLayout()
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("color: #ffffff;")
        mode_row.addWidget(mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["sequence", "date", "replace", "lowercase", "uppercase", "clean"])
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)
        mode_row.addWidget(self.mode_combo)
        mode_row.addStretch()
        options_layout.addLayout(mode_row)

        # Mode-specific options
        self.mode_options_widget = QWidget()
        self.mode_options_layout = QHBoxLayout(self.mode_options_widget)
        self._setup_mode_options("sequence")
        options_layout.addWidget(self.mode_options_widget)

        # Pattern filter
        pattern_row = QHBoxLayout()
        pattern_label = QLabel("Filter pattern:")
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
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        pattern_row.addWidget(self.pattern_input)
        pattern_row.addStretch()
        options_layout.addLayout(pattern_row)

        # Recursive checkbox
        self.recursive_check = QCheckBox("Recursive (include subdirectories)")
        self.recursive_check.setChecked(False)
        options_layout.addWidget(self.recursive_check)

        self.main_layout.addWidget(options_group)

        # Preview table
        preview_group = QGroupBox("Preview")
        preview_group.setStyleSheet(dir_group.styleSheet())
        preview_layout = QVBoxLayout(preview_group)

        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)
        self.preview_table.setHorizontalHeaderLabels(["Original Name", "New Name"])
        self.preview_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.preview_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.preview_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                gridline-color: #3d3d3d;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                padding: 5px;
            }
        """)
        preview_layout.addWidget(self.preview_table)

        self.preview_count_label = QLabel("0 files")
        self.preview_count_label.setStyleSheet("color: #888888;")
        preview_layout.addWidget(self.preview_count_label)

        self.main_layout.addWidget(preview_group)

        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.preview_btn = self.add_button("Preview", self._generate_preview)
        action_layout.addWidget(self.preview_btn)

        self.execute_btn = self.add_button("Execute", self._execute_rename, primary=True)
        self.execute_btn.setEnabled(False)
        action_layout.addWidget(self.execute_btn)

        self.undo_btn = self.add_button("Undo Last", self._undo_last)
        action_layout.addWidget(self.undo_btn)

        self.main_layout.addLayout(action_layout)

    def _setup_mode_options(self, mode: str):
        """Setup mode-specific options."""
        # Clear existing options
        while self.mode_options_layout.count():
            child = self.mode_options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if mode == "sequence":
            # Start number
            start_label = QLabel("Start:")
            start_label.setStyleSheet("color: #ffffff;")
            self.mode_options_layout.addWidget(start_label)

            self.start_spin = QSpinBox()
            self.start_spin.setRange(0, 99999)
            self.start_spin.setValue(1)
            self.start_spin.setStyleSheet("""
                QSpinBox {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #4d4d4d;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)
            self.mode_options_layout.addWidget(self.start_spin)

            # Padding
            padding_label = QLabel("Padding:")
            padding_label.setStyleSheet("color: #ffffff;")
            self.mode_options_layout.addWidget(padding_label)

            self.padding_spin = QSpinBox()
            self.padding_spin.setRange(1, 10)
            self.padding_spin.setValue(3)
            self.padding_spin.setStyleSheet(self.start_spin.styleSheet())
            self.mode_options_layout.addWidget(self.padding_spin)

        elif mode == "replace":
            # Find text
            find_label = QLabel("Find:")
            find_label.setStyleSheet("color: #ffffff;")
            self.mode_options_layout.addWidget(find_label)

            self.find_input = QLineEdit()
            self.find_input.setPlaceholderText("Text to find")
            self.find_input.setStyleSheet("""
                QLineEdit {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #4d4d4d;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)
            self.mode_options_layout.addWidget(self.find_input)

            # Replace with
            replace_label = QLabel("Replace:")
            replace_label.setStyleSheet("color: #ffffff;")
            self.mode_options_layout.addWidget(replace_label)

            self.replace_input = QLineEdit()
            self.replace_input.setPlaceholderText("Replacement text")
            self.replace_input.setStyleSheet(self.find_input.styleSheet())
            self.mode_options_layout.addWidget(self.replace_input)

            # Regex checkbox
            self.regex_check = QCheckBox("Regex")
            self.mode_options_layout.addWidget(self.regex_check)

        self.mode_options_layout.addStretch()

    def _on_mode_changed(self, mode: str):
        """Handle mode change."""
        self._setup_mode_options(mode)
        self._generate_preview()

    def _browse_directory(self):
        """Browse for directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            "",
            QFileDialog.ShowDirsOnly
        )

        if directory:
            self.selected_directory = Path(directory)
            self.dir_label.setText(str(self.selected_directory))
            self.dir_label.setStyleSheet("color: #ffffff;")
            self._generate_preview()

    def _generate_preview(self):
        """Generate preview of rename operations."""
        if not self.selected_directory:
            return

        if not CLI_AVAILABLE:
            QMessageBox.warning(
                self,
                "CLI Not Available",
                "SmartRename CLI backend is not installed.\nPlease install it first: pip install smartrename"
            )
            return

        mode = self.mode_combo.currentText()
        pattern = self.pattern_input.text() or None
        recursive = self.recursive_check.isChecked()

        # Get mode-specific kwargs
        kwargs = {}
        if mode == "sequence":
            kwargs["start"] = self.start_spin.value()
            kwargs["padding"] = self.padding_spin.value()
        elif mode == "replace":
            kwargs["find"] = self.find_input.text()
            kwargs["replace_with"] = self.replace_input.text()
            kwargs["regex"] = self.regex_check.isChecked()

        # Run preview worker
        self.preview_btn.setEnabled(False)
        self.preview_btn.setText("Loading...")

        self.preview_worker = PreviewWorker(
            self.selected_directory, mode, pattern, recursive, **kwargs
        )
        self.preview_worker.finished.connect(self._display_preview)
        self.preview_worker.error.connect(self._on_preview_error)
        self.preview_worker.start()

    def _on_preview_error(self, error_msg: str):
        """Handle preview error."""
        self.preview_btn.setEnabled(True)
        self.preview_btn.setText("Preview")
        QMessageBox.warning(self, "Preview Error", error_msg)

    def _display_preview(self, operations: List[Dict]):
        """Display preview results in table."""
        self.preview_btn.setEnabled(True)
        self.preview_btn.setText("Preview")

        self.preview_operations = operations
        self.preview_table.setRowCount(len(operations))

        for row, op in enumerate(operations):
            old_item = QTableWidgetItem(op.get("old_name", op.get("old_path", "").split("/")[-1]))
            new_item = QTableWidgetItem(op.get("new_name", op.get("new_path", "").split("/")[-1]))

            # Highlight changes
            if old_item.text() != new_item.text():
                new_item.setForeground(QColor("#0078d4"))

            self.preview_table.setItem(row, 0, old_item)
            self.preview_table.setItem(row, 1, new_item)

        self.preview_count_label.setText(f"{len(operations)} files")
        self.execute_btn.setEnabled(len(operations) > 0)

    def _execute_rename(self):
        """Execute the rename operations."""
        if not self.selected_directory or not self.preview_operations:
            return

        mode = self.mode_combo.currentText()
        pattern = self.pattern_input.text() or None
        recursive = self.recursive_check.isChecked()

        kwargs = {}
        if mode == "sequence":
            kwargs["start"] = self.start_spin.value()
            kwargs["padding"] = self.padding_spin.value()

        result = rename_directory(
            self.selected_directory,
            mode,
            pattern,
            recursive,
            dry_run=False,
            skip_confirm=True,
            **kwargs
        )

        if result["success"]:
            QMessageBox.information(
                self,
                "Success",
                f"Renamed {result['count']} files successfully.\nSession ID: {result.get('session_id', 'N/A')}"
            )
            self._generate_preview()
        else:
            QMessageBox.warning(
                self,
                "Error",
                f"Rename failed: {result.get('errors', ['Unknown error'])}"
            )

    def _undo_last(self):
        """Undo the last rename operation."""
        if not CLI_AVAILABLE:
            return

        try:
            from smartrename.core.undo import undo_last_session
            result = undo_last_session()

            if result:
                QMessageBox.information(
                    self,
                    "Undo Successful",
                    f"Undid {result['count']} rename operations."
                )
                self._generate_preview()
            else:
                QMessageBox.warning(self, "No History", "No undo history available.")
        except ImportError:
            QMessageBox.warning(self, "Error", "Undo functionality not available.")