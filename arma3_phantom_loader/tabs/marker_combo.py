"""A shared "type-or-select" marker-name widget.

An editable QComboBox whose drop-down lists the markers parsed from the
mission's mission.sqm, while still letting the author type a name that does not
exist yet (a marker they intend to place in Eden later). `currentText()` returns
whatever was typed or picked, so callers treat it like a line edit.
"""
from __future__ import annotations

from typing import List

from PySide6.QtWidgets import QComboBox, QCompleter


def make_marker_combo(placeholder: str = "Marker name") -> QComboBox:
    combo = QComboBox()
    combo.setEditable(True)
    combo.setInsertPolicy(QComboBox.NoInsert)
    combo.lineEdit().setPlaceholderText(placeholder)
    combo.setCompleter(QCompleter(combo.model(), combo))
    return combo


def set_marker_items(combo: QComboBox, names: List[str]) -> None:
    """Repopulate the drop-down list, preserving the current text."""
    current = combo.currentText()
    combo.clear()
    combo.addItems(names)
    combo.setCurrentText(current)
