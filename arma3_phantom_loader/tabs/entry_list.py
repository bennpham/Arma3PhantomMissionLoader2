"""Shared add/update/remove list editor used by the debriefing, briefing and
task tabs."""
from __future__ import annotations

from typing import List, Optional

from PySide6.QtWidgets import (QHBoxLayout, QListWidget, QMessageBox,
                               QPushButton, QVBoxLayout, QWidget)


class EntryListTab(QWidget):
    """Left: list of entries. Right: a form provided by the subclass.

    Subclasses implement:
      _build_form(layout)      populate the right-hand form
      _make_entry()            build an entry object from the form (or raise
                               ValueError with a user-facing message)
      _load_entry(entry)       fill the form from an entry
      _label(entry)            list row text
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.entries: List = []

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self._row_changed)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self._add)
        update_button = QPushButton("Update selected")
        update_button.clicked.connect(self._update)
        remove_button = QPushButton("Remove selected")
        remove_button.clicked.connect(self._remove)

        buttons = QHBoxLayout()
        buttons.addWidget(add_button)
        buttons.addWidget(update_button)
        buttons.addWidget(remove_button)
        buttons.addStretch()

        left = QVBoxLayout()
        left.addWidget(self.list_widget)

        self.form_layout = QVBoxLayout()
        self._build_form(self.form_layout)
        self.form_layout.addLayout(buttons)
        self.form_layout.addStretch()

        layout = QHBoxLayout(self)
        layout.addLayout(left, 1)
        layout.addLayout(self.form_layout, 2)

    # ------------------------------------------------------------------ api
    def _build_form(self, layout: QVBoxLayout) -> None:
        raise NotImplementedError

    def _make_entry(self, updating_row: Optional[int] = None):
        raise NotImplementedError

    def _load_entry(self, entry) -> None:
        raise NotImplementedError

    def _label(self, entry) -> str:
        raise NotImplementedError

    # -------------------------------------------------------------- actions
    def _selected_row(self) -> Optional[int]:
        row = self.list_widget.currentRow()
        return row if 0 <= row < len(self.entries) else None

    def _add(self) -> None:
        try:
            entry = self._make_entry()
        except ValueError as error:
            QMessageBox.critical(self, "Invalid entry", str(error))
            return
        self.entries.append(entry)
        self.list_widget.addItem(self._label(entry))
        self.list_widget.setCurrentRow(len(self.entries) - 1)

    def _update(self) -> None:
        row = self._selected_row()
        if row is None:
            return
        try:
            entry = self._make_entry(updating_row=row)
        except ValueError as error:
            QMessageBox.critical(self, "Invalid entry", str(error))
            return
        self.entries[row] = entry
        self.list_widget.item(row).setText(self._label(entry))

    def _remove(self) -> None:
        row = self._selected_row()
        if row is None:
            return
        self.entries.pop(row)
        self.list_widget.takeItem(row)

    def _row_changed(self, row: int) -> None:
        if 0 <= row < len(self.entries):
            self._load_entry(self.entries[row])
