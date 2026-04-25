"""DirSnap GUI panel."""

from pathlib import Path
from typing import List, Dict
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QCheckBox, QTextEdit,
    QTreeWidget, QTreeWidgetItem, QFileDialog,
    QGroupBox, QMessageBox, QSplitter, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

# Import CLI backend
import sys
_bundle_path = Path(__file__).parent.parent.parent.parent.parent
dirsnap_path = _bundle_path / "dirsnap"
if dirsnap_path not in sys.path:
    sys.path.insert(0, str(dirsnap_path))

try:
    from dirsnap.core.scanner import scan_directory
    from dirsnap.core.renderer import render_tree, render_markdown, render_json, render_html
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False

from gui.widgets.base_panel import BasePanel


class DirSnapPanel(BasePanel):
    """GUI panel for DirSnap directory snapshot tool."""

    tool_name = "DirSnap"
    tool_icon = "🌳"
    tool_description = "Directory structure snapshots in multiple formats"

    def __init__(self, parent=None):
        self.selected_directory = None
        self.scan_result = None
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

        # Options
        options_group = QGroupBox("Options")
        options_group.setStyleSheet(dir_group.styleSheet())
        options_layout = QVBoxLayout(options_group)

        # Format selection
        format_row = QHBoxLayout()
        format_label = QLabel("Output format:")
        format_label.setStyleSheet("color: #ffffff;")
        format_row.addWidget(format_label)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["Tree", "Markdown", "JSON", "HTML"])
        format_row.addWidget(self.format_combo)
        format_row.addStretch()
        options_layout.addLayout(format_row)

        # Recursive checkbox
        self.recursive_check = QCheckBox("Recursive (default)")
        self.recursive_check.setChecked(True)
        options_layout.addWidget(self.recursive_check)

        # Show hidden checkbox
        self.hidden_check = QCheckBox("Show hidden files (.git, .env)")
        self.hidden_check.setChecked(False)
        options_layout.addWidget(self.hidden_check)

        # Exclude patterns
        exclude_row = QHBoxLayout()
        exclude_label = QLabel("Exclude:")
        exclude_label.setStyleSheet("color: #ffffff;")
        exclude_row.addWidget(exclude_label)

        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText("node_modules, .git (comma-separated)")
        self.exclude_input.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        exclude_row.addWidget(self.exclude_input)
        options_layout.addLayout(exclude_row)

        self.main_layout.addWidget(options_group)

        # Output area with splitter
        splitter = QSplitter(Qt.Vertical)

        # Tree view
        tree_group = QGroupBox("Directory Tree")
        tree_group.setStyleSheet(dir_group.styleSheet())
        tree_layout = QVBoxLayout(tree_group)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Name", "Size", "Type"])
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
            }
            QTreeWidget::item {
                padding: 3px;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
            }
        """)
        tree_layout.addWidget(self.tree_widget)

        splitter.addWidget(tree_group)

        # Output text
        output_group = QGroupBox("Output")
        output_group.setStyleSheet(dir_group.styleSheet())
        output_layout = QVBoxLayout(output_group)

        self.output_text = QTextEdit()
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)
        self.output_text.setFont(QFont("Consolas", 10))
        output_layout.addWidget(self.output_text)

        splitter.addWidget(output_group)

        self.main_layout.addWidget(splitter, stretch=1)

        # Action buttons
        action_layout = QHBoxLayout()

        self.scan_btn = self.add_button("Scan", self._scan_directory, primary=True)
        action_layout.addWidget(self.scan_btn)

        self.export_btn = self.add_button("Export", self._export_output)
        action_layout.addWidget(self.export_btn)

        action_layout.addStretch()

        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("color: #888888;")
        action_layout.addWidget(self.stats_label)

        self.main_layout.addLayout(action_layout)

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
            self._scan_directory()

    def _scan_directory(self):
        """Scan the selected directory."""
        if not self.selected_directory:
            QMessageBox.warning(self, "No Directory", "Please select a directory first.")
            return

        if not CLI_AVAILABLE:
            QMessageBox.warning(
                self,
                "CLI Not Available",
                "DirSnap CLI backend is not installed.\nPlease install: pip install dirsnap"
            )
            return

        # Get options
        excludes = []
        if self.exclude_input.text():
            excludes = [e.strip() for e in self.exclude_input.text().split(",")]

        # Scan directory
        self.scan_result = scan_directory(
            self.selected_directory,
            recursive=self.recursive_check.isChecked(),
            include_hidden=self.hidden_check.isChecked(),
            excludes=excludes
        )

        # Display tree
        self._display_tree()

        # Generate output
        self._generate_output()

        # Update stats
        self.stats_label.setText(
            f"{self.scan_result['stats']['file_count']} files | "
            f"{self.scan_result['stats']['dir_count']} dirs | "
            f"{self.scan_result['stats']['total_size'] / 1024:.1f} KB"
        )

    def _display_tree(self):
        """Display directory tree in tree widget."""
        self.tree_widget.clear()

        if not self.scan_result:
            return

        root_item = QTreeWidgetItem([self.selected_directory.name, "", "Directory"])
        root_item.setForeground(0, QColor("#0078d4"))
        self.tree_widget.addTopLevelItem(root_item)

        self._add_tree_items(root_item, self.scan_result["tree"])

        self.tree_widget.expandItem(root_item)

    def _add_tree_items(self, parent_item: QTreeWidgetItem, items: List[Dict]):
        """Add tree items recursively."""
        for item in items:
            if item["type"] == "directory":
                dir_item = QTreeWidgetItem([item["name"], "", "Directory"])
                dir_item.setForeground(0, QColor("#00d400"))
                parent_item.addChild(dir_item)
                if item["children"]:
                    self._add_tree_items(dir_item, item["children"])
            else:
                size_str = f"{item['size'] / 1024:.1f} KB" if item['size'] < 1024 * 1024 else f"{item['size'] / 1024 / 1024:.2f} MB"
                file_item = QTreeWidgetItem([item["name"], size_str, item["ext"]])
                parent_item.addChild(file_item)

    def _generate_output(self):
        """Generate output in selected format."""
        if not self.scan_result:
            return

        format_map = {
            "Tree": render_tree,
            "Markdown": render_markdown,
            "JSON": render_json,
            "HTML": render_html,
        }

        format_name = self.format_combo.currentText()
        renderer = format_map[format_name]

        output = renderer(self.scan_result)
        self.output_text.setText(output)

    def _export_output(self):
        """Export output to file."""
        if not self.output_text.text():
            QMessageBox.warning(self, "No Output", "Please scan a directory first.")
            return

        format_name = self.format_combo.currentText()
        ext_map = {"Tree": ".txt", "Markdown": ".md", "JSON": ".json", "HTML": ".html"}

        default_name = f"directory_snapshot{ext_map[format_name]}"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Output",
            default_name,
            f"{format_name} Files (*{ext_map[format_name]})"
        )

        if file_path:
            Path(file_path).write_text(self.output_text.text())
            QMessageBox.information(self, "Exported", f"Exported to {file_path}")