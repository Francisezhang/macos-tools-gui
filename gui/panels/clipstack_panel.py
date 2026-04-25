"""ClipStack GUI panel."""

from pathlib import Path
from typing import List, Dict
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QCheckBox, QMessageBox, QComboBox, QWidget
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont

# Import CLI backend
import sys
_bundle_path = Path(__file__).parent.parent.parent.parent.parent
clipstack_path = _bundle_path / "clipstack"
if clipstack_path not in sys.path:
    sys.path.insert(0, str(clipstack_path))

try:
    from clipstack.core.storage import (
        get_entries, get_entry_by_id, get_last_entry,
        search_entries, pin_entry, unpin_entry, delete_entry,
        get_stats, clear_history, ensure_db
    )
    from clipstack.core.monitor import start_daemon, stop_daemon, is_running, get_auto_start_status
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False

from gui.widgets.base_panel import BasePanel


class ClipStackPanel(BasePanel):
    """GUI panel for ClipStack clipboard history manager."""

    tool_name = "ClipStack"
    tool_icon = "📋"
    tool_description = "Clipboard history with search and pin support"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._refresh_timer = QTimer()
        self._refresh_timer.timeout.connect(self._refresh_history)
        self._refresh_timer.start(2000)  # Refresh every 2 seconds

    def _setup_content(self):
        """Setup panel content."""
        # Daemon status
        daemon_group = QGroupBox("Daemon Status")
        daemon_group.setStyleSheet("""
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
        daemon_layout = QHBoxLayout(daemon_group)

        self.status_label = QLabel("Checking...")
        self.status_label.setStyleSheet("color: #888888;")
        daemon_layout.addWidget(self.status_label, stretch=1)

        self.start_btn = self.add_button("Start", self._start_daemon)
        daemon_layout.addWidget(self.start_btn)

        self.stop_btn = self.add_button("Stop", self._stop_daemon)
        daemon_layout.addWidget(self.stop_btn)

        self.main_layout.addWidget(daemon_group)

        # Search bar
        search_group = QGroupBox("Search")
        search_group.setStyleSheet(daemon_group.styleSheet())
        search_layout = QHBoxLayout(search_group)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search clipboard history...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        self.search_input.textChanged.connect(self._search_history)
        search_layout.addWidget(self.search_input, stretch=1)

        # Type filter
        self.type_combo = QComboBox()
        self.type_combo.addItems(["All", "URL", "Code", "Text"])
        self.type_combo.currentTextChanged.connect(self._filter_by_type)
        search_layout.addWidget(self.type_combo)

        self.main_layout.addWidget(search_group)

        # History table
        history_group = QGroupBox("Clipboard History")
        history_group.setStyleSheet(daemon_group.styleSheet())
        history_layout = QVBoxLayout(history_group)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["ID", "Type", "Preview", "Pinned"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SingleSelection)
        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                gridline-color: #3d3d3d;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
            }
            QHeaderView::section {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                padding: 5px;
            }
        """)
        self.history_table.cellClicked.connect(self._on_row_selected)
        history_layout.addWidget(self.history_table)

        # Stats label
        self.stats_label = QLabel("0 entries")
        self.stats_label.setStyleSheet("color: #888888;")
        history_layout.addWidget(self.stats_label)

        self.main_layout.addWidget(history_group)

        # Action buttons
        action_layout = QHBoxLayout()

        self.copy_btn = self.add_button("Copy Selected", self._copy_selected, primary=True)
        action_layout.addWidget(self.copy_btn)

        self.pin_btn = self.add_button("Pin", self._pin_selected)
        action_layout.addWidget(self.pin_btn)

        self.delete_btn = self.add_button("Delete", self._delete_selected)
        action_layout.addWidget(self.delete_btn)

        action_layout.addStretch()

        self.clear_btn = self.add_button("Clear All", self._clear_history)
        action_layout.addWidget(self.clear_btn)

        self.main_layout.addLayout(action_layout)

        # Initial refresh
        self._refresh_status()
        self._refresh_history()

    def _refresh_status(self):
        """Refresh daemon status."""
        if not CLI_AVAILABLE:
            self.status_label.setText("CLI not available")
            self.status_label.setStyleSheet("color: #ff4444;")
            return

        running = is_running()
        if running:
            self.status_label.setText("🟢 Running")
            self.status_label.setStyleSheet("color: #00d400;")
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        else:
            self.status_label.setText("🔴 Stopped")
            self.status_label.setStyleSheet("color: #ff4444;")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    def _refresh_history(self):
        """Refresh clipboard history table."""
        if not CLI_AVAILABLE:
            return

        ensure_db()
        entries = get_entries(limit=50)
        self._display_entries(entries)

        # Update stats
        stats = get_stats()
        self.stats_label.setText(
            f"{stats['total_entries']} entries | {stats['pinned_entries']} pinned"
        )

    def _display_entries(self, entries: List[Dict]):
        """Display entries in table."""
        self.history_table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            id_item = QTableWidgetItem(str(entry["id"]))
            id_item.setData(Qt.UserRole, entry["id"])

            type_item = QTableWidgetItem(entry["type"])
            if entry["type"] == "url":
                type_item.setForeground(QColor("#0078d4"))
            elif entry["type"] == "code":
                type_item.setForeground(QColor("#00d400"))

            # Preview (truncate long content)
            preview = entry["content"][:50] + "..." if len(entry["content"]) > 50 else entry["content"]
            preview_item = QTableWidgetItem(preview)

            pinned_item = QTableWidgetItem("📌" if entry["is_pinned"] else "")
            pinned_item.setForeground(QColor("#ffaa00"))

            self.history_table.setItem(row, 0, id_item)
            self.history_table.setItem(row, 1, type_item)
            self.history_table.setItem(row, 2, preview_item)
            self.history_table.setItem(row, 3, pinned_item)

    def _search_history(self, keyword: str):
        """Search clipboard history."""
        if not CLI_AVAILABLE:
            return

        if keyword.strip():
            try:
                entries = search_entries(keyword, limit=50)
                self._display_entries(entries)
            except Exception:
                pass
        else:
            self._refresh_history()

    def _filter_by_type(self, type_filter: str):
        """Filter by entry type."""
        if not CLI_AVAILABLE:
            return

        type_map = {"All": "all", "URL": "url", "Code": "code", "Text": "text"}
        entries = get_entries(limit=50, entry_type=type_map[type_filter])
        self._display_entries(entries)

    def _on_row_selected(self, row: int, column: int):
        """Handle row selection."""
        pass

    def _copy_selected(self):
        """Copy selected entry to clipboard."""
        selected_rows = self.history_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select an entry to copy.")
            return

        row = selected_rows[0].row()
        id_item = self.history_table.item(row, 0)
        entry_id = id_item.data(Qt.UserRole)

        entry = get_entry_by_id(entry_id)
        if entry:
            try:
                import pyperclip
                pyperclip.copy(entry["content"])
                QMessageBox.information(self, "Copied", "Content copied to clipboard!")
            except ImportError:
                QMessageBox.warning(self, "Error", "pyperclip not installed")

    def _pin_selected(self):
        """Pin selected entry."""
        selected_rows = self.history_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        id_item = self.history_table.item(row, 0)
        entry_id = id_item.data(Qt.UserRole)

        pinned_item = self.history_table.item(row, 3)
        is_pinned = pinned_item.text() == "📌"

        if is_pinned:
            unpin_entry(entry_id)
            pinned_item.setText("")
        else:
            pin_entry(entry_id)
            pinned_item.setText("📌")

    def _delete_selected(self):
        """Delete selected entry."""
        selected_rows = self.history_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        id_item = self.history_table.item(row, 0)
        entry_id = id_item.data(Qt.UserRole)

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            delete_entry(entry_id)
            self._refresh_history()

    def _clear_history(self):
        """Clear all history."""
        confirm = QMessageBox.question(
            self,
            "Confirm Clear",
            "Clear all clipboard history?\n(Pinned entries will be preserved)",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            clear_history(keep_pinned=True)
            self._refresh_history()

    def _start_daemon(self):
        """Start clipboard daemon."""
        if not CLI_AVAILABLE:
            return

        if start_daemon():
            QMessageBox.information(self, "Started", "Daemon started successfully!")
            self._refresh_status()
        else:
            QMessageBox.warning(self, "Error", "Failed to start daemon.")

    def _stop_daemon(self):
        """Stop clipboard daemon."""
        if not CLI_AVAILABLE:
            return

        if stop_daemon():
            QMessageBox.information(self, "Stopped", "Daemon stopped.")
            self._refresh_status()