"""EnvGuard GUI panel."""

from pathlib import Path
from typing import List, Dict
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QGroupBox, QMessageBox, QTextEdit, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

# Import CLI backend
import sys
_bundle_path = Path(__file__).parent.parent.parent.parent.parent
envguard_path = _bundle_path / "envguard"
if envguard_path not in sys.path:
    sys.path.insert(0, str(envguard_path))

try:
    from envguard.core.vault import list_entries, add_to_vault, get_entry, get_entry_content, delete_entry
    from envguard.core.crypto import encrypt, decrypt
    from envguard.utils.scanner import scan_for_env_files
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False

from gui.widgets.base_panel import BasePanel


class EnvGuardPanel(BasePanel):
    """GUI panel for EnvGuard .env backup tool."""

    tool_name = "EnvGuard"
    tool_icon = "🔐"
    tool_description = "AES-256-GCM encrypted .env backup"

    def __init__(self, parent=None):
        self.password = None
        super().__init__(parent)

    def _setup_content(self):
        """Setup panel content."""
        # Password setup
        password_group = QGroupBox("Master Password")
        password_group.setStyleSheet("""
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
        password_layout = QHBoxLayout(password_group)

        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: #ffffff;")
        password_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter master password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        password_layout.addWidget(self.password_input, stretch=1)

        self.unlock_btn = self.add_button("Unlock", self._unlock_vault)
        password_layout.addWidget(self.unlock_btn)

        self.main_layout.addWidget(password_group)

        # Vault entries
        vault_group = QGroupBox("Vault Entries")
        vault_group.setStyleSheet(password_group.styleSheet())
        vault_layout = QVBoxLayout(vault_group)

        self.vault_table = QTableWidget()
        self.vault_table.setColumnCount(4)
        self.vault_table.setHorizontalHeaderLabels(["ID", "Name", "Project", "Created"])
        self.vault_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.vault_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.vault_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.vault_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.vault_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.vault_table.setStyleSheet("""
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
        vault_layout.addWidget(self.vault_table)

        self.entry_count_label = QLabel("0 entries")
        self.entry_count_label.setStyleSheet("color: #888888;")
        vault_layout.addWidget(self.entry_count_label)

        self.main_layout.addWidget(vault_group)

        # Content viewer
        content_group = QGroupBox("Entry Content")
        content_group.setStyleSheet(password_group.styleSheet())
        content_layout = QVBoxLayout(content_group)

        self.content_text = QTextEdit()
        self.content_text.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)
        self.content_text.setFont(QFont("Consolas", 10))
        self.content_text.setPlaceholderText("Select an entry to view content")
        content_layout.addWidget(self.content_text)

        self.main_layout.addWidget(content_group)

        # Scanner section
        scan_group = QGroupBox("Scanner")
        scan_group.setStyleSheet(password_group.styleSheet())
        scan_layout = QHBoxLayout(scan_group)

        self.scan_dir_label = QLabel("No directory selected")
        self.scan_dir_label.setStyleSheet("color: #888888;")
        scan_layout.addWidget(self.scan_dir_label, stretch=1)

        self.scan_browse_btn = self.add_button("Browse...", self._browse_scan_dir)
        scan_layout.addWidget(self.scan_browse_btn)

        self.scan_btn = self.add_button("Scan", self._scan_for_env)
        scan_layout.addWidget(self.scan_btn)

        self.main_layout.addWidget(scan_group)

        # Action buttons
        action_layout = QHBoxLayout()

        self.add_btn = self.add_button("Add .env", self._add_env_file)
        action_layout.addWidget(self.add_btn)

        self.get_btn = self.add_button("Get Selected", self._get_selected_entry, primary=True)
        action_layout.addWidget(self.get_btn)

        self.delete_btn = self.add_button("Delete", self._delete_selected)
        action_layout.addWidget(self.delete_btn)

        self.sync_btn = self.add_button("Sync to Cloud", self._sync_to_cloud)
        action_layout.addWidget(self.sync_btn)

        self.main_layout.addLayout(action_layout)

        # Initial load
        self._refresh_vault()

    def _unlock_vault(self):
        """Unlock vault with password."""
        self.password = self.password_input.text()
        if not self.password:
            QMessageBox.warning(self, "No Password", "Please enter a password.")
            return

        self._refresh_vault()
        self.content_text.setPlaceholderText("Vault unlocked. Select an entry to view.")

    def _refresh_vault(self):
        """Refresh vault entries list."""
        if not CLI_AVAILABLE:
            self.entry_count_label.setText("CLI not available")
            return

        entries = list_entries()
        self.vault_table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            id_item = QTableWidgetItem(entry["id"])
            name_item = QTableWidgetItem(entry["name"])
            project_item = QTableWidgetItem(entry["project"])
            created_item = QTableWidgetItem(entry["created_at"][:10])

            self.vault_table.setItem(row, 0, id_item)
            self.vault_table.setItem(row, 1, name_item)
            self.vault_table.setItem(row, 2, project_item)
            self.vault_table.setItem(row, 3, created_item)

        self.entry_count_label.setText(f"{len(entries)} entries")

    def _add_env_file(self):
        """Add a .env file to vault."""
        if not self.password:
            QMessageBox.warning(self, "No Password", "Please unlock vault first.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select .env File",
            "",
            "Environment Files (*.env);;All Files (*)"
        )

        if file_path:
            name = Path(file_path).stem

            # Read and encrypt
            content = Path(file_path).read_text()
            encrypted = encrypt(content, self.password)

            # Add to vault
            entry = add_to_vault(Path(file_path), encrypted, name=name)

            QMessageBox.information(
                self,
                "Added",
                f"Added {name} to vault.\nEntry ID: {entry['id']}"
            )

            self._refresh_vault()

    def _get_selected_entry(self):
        """Get and decrypt selected entry."""
        if not self.password:
            QMessageBox.warning(self, "No Password", "Please unlock vault first.")
            return

        selected = self.vault_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select an entry.")
            return

        row = selected[0].row()
        id_item = self.vault_table.item(row, 0)
        entry_id = id_item.text()

        entry = get_entry(entry_id)
        if entry:
            try:
                content = get_entry_content(entry, self.password)
                self.content_text.setText(content)
            except Exception as e:
                QMessageBox.warning(self, "Decryption Failed", str(e))

    def _delete_selected(self):
        """Delete selected entry."""
        selected = self.vault_table.selectedItems()
        if not selected:
            return

        row = selected[0].row()
        id_item = self.vault_table.item(row, 0)
        entry_id = id_item.text()

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete entry {entry_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            delete_entry(entry_id)
            self._refresh_vault()
            self.content_text.clear()

    def _browse_scan_dir(self):
        """Browse directory to scan."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory to Scan",
            "",
            QFileDialog.ShowDirsOnly
        )

        if directory:
            self.scan_dir_label.setText(directory)
            self.scan_dir_label.setStyleSheet("color: #ffffff;")

    def _scan_for_env(self):
        """Scan directory for .env files."""
        if not self.scan_dir_label.text() or self.scan_dir_label.text() == "No directory selected":
            QMessageBox.warning(self, "No Directory", "Please select a directory to scan.")
            return

        if not CLI_AVAILABLE:
            return

        scan_path = Path(self.scan_dir_label.text())
        results = scan_for_env_files(scan_path)

        # Show results
        warnings = results.get("warnings", [])
        env_files = results.get("files", [])

        msg = f"Found {len(env_files)} .env files"
        if warnings:
            msg += f"\n⚠️ {len(warnings)} warnings (not in .gitignore)"

        QMessageBox.information(self, "Scan Results", msg)

    def _sync_to_cloud(self):
        """Sync vault to cloud storage."""
        if not CLI_AVAILABLE:
            return

        try:
            from envguard.core.vault import sync_to_cloud
            sync_to_cloud()
            QMessageBox.information(self, "Synced", "Vault synced to cloud storage.")
        except Exception as e:
            QMessageBox.warning(self, "Sync Failed", str(e))