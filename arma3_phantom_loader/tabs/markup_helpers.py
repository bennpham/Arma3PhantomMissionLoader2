"""Shared widget that inserts FHQ briefing markup (colored text / marker
links) into a description editor, mirroring the original Text/Color/Marker
helper buttons."""
from __future__ import annotations

import re
from typing import List

from PySide6.QtWidgets import (QColorDialog, QGridLayout, QGroupBox,
                               QLineEdit, QMessageBox, QPlainTextEdit,
                               QPushButton)

from .marker_combo import make_marker_combo, set_marker_items

HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def is_hex_color(text: str) -> bool:
    return bool(HEX_COLOR_RE.match(text))


def _esc(text: str) -> str:
    return text.replace('"', '""')


class MarkupHelperBox(QGroupBox):
    """Appends font-color / marker-link markup to a target text editor."""

    def __init__(self, target: QPlainTextEdit, parent=None):
        super().__init__("Insert markup into description", parent)
        self._target = target

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Text to insert")
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("#FF0000")
        self.marker_input = make_marker_combo("Marker name")

        pick_button = QPushButton("Pick color…")
        pick_button.clicked.connect(self._pick_color)

        text_button = QPushButton("Text (UI color)")
        text_button.clicked.connect(self._insert_text_default)
        ctext_button = QPushButton("Text (custom color)")
        ctext_button.clicked.connect(self._insert_text_custom)
        link_button = QPushButton("Marker link (UI color)")
        link_button.clicked.connect(self._insert_link_default)
        clink_button = QPushButton("Marker link (custom color)")
        clink_button.clicked.connect(self._insert_link_custom)

        grid = QGridLayout(self)
        grid.addWidget(self.text_input, 0, 0, 1, 2)
        grid.addWidget(self.color_input, 0, 2)
        grid.addWidget(pick_button, 0, 3)
        grid.addWidget(self.marker_input, 1, 0, 1, 2)
        grid.addWidget(text_button, 2, 0)
        grid.addWidget(ctext_button, 2, 1)
        grid.addWidget(link_button, 2, 2)
        grid.addWidget(clink_button, 2, 3)

    # ------------------------------------------------------------- helpers
    def _append(self, markup: str) -> None:
        self._target.setPlainText(self._target.toPlainText() + markup)

    def _pick_color(self) -> None:
        color = QColorDialog.getColor(parent=self)
        if color.isValid():
            self.color_input.setText(color.name().upper())

    def _valid_color(self) -> bool:
        if not is_hex_color(self.color_input.text()):
            QMessageBox.critical(
                self, "Invalid Color",
                "Color in hexadecimal format is required! "
                "Please input a string like #FF0000 to define the color.")
            return False
        return True

    def set_markers(self, names: List[str]) -> None:
        set_marker_items(self.marker_input, names)

    def _valid_marker(self) -> bool:
        marker = self.marker_input.currentText()
        if "'" in marker or '"' in marker:
            QMessageBox.critical(
                self, "Quotes not Allowed",
                "Marker name must not contain any quotes, whether ' or \".")
            return False
        return True

    # ------------------------------------------------------------- actions
    def _insert_text_default(self) -> None:
        self._append("<font color='\" + _htmlcolor + \"'>"
                     + _esc(self.text_input.text()) + "</font>")

    def _insert_text_custom(self) -> None:
        if self._valid_color():
            self._append(f"<font color='{self.color_input.text()}'>"
                         + _esc(self.text_input.text()) + "</font>")

    def _insert_link_default(self) -> None:
        if self._valid_marker():
            self._append("<font color='\" + _htmlcolor + \"'>"
                         f"<marker name='{self.marker_input.currentText()}'>"
                         + _esc(self.text_input.text()) + "</marker></font>")

    def _insert_link_custom(self) -> None:
        if self._valid_color() and self._valid_marker():
            self._append(f"<font color='{self.color_input.text()}'>"
                         f"<marker name='{self.marker_input.currentText()}'>"
                         + _esc(self.text_input.text()) + "</marker></font>")
