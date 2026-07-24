"""Tab 5: briefing entries loaded by FHQ TaskTracker (FHQ_fnc_ttAddBriefing)."""
from __future__ import annotations

from typing import List, Optional

from PySide6.QtWidgets import (QFormLayout, QLabel, QLineEdit, QPlainTextEdit,
                               QVBoxLayout)

from ..model import BriefingEntry, MissionConfig
from .entry_list import EntryListTab
from .markup_helpers import MarkupHelperBox


class BriefingTab(EntryListTab):
    def _build_form(self, layout: QVBoxLayout) -> None:
        layout.addWidget(QLabel(
            "Briefing sections shown in the map screen (diary). Added in order."))
        form = QFormLayout()
        self.title = QLineEdit()
        self.description = QPlainTextEdit()
        form.addRow("Title", self.title)
        form.addRow("Description", self.description)
        layout.addLayout(form)
        self.markup = MarkupHelperBox(self.description)
        layout.addWidget(self.markup)

    def set_markers(self, names: List[str]) -> None:
        self.markup.set_markers(names)

    def _make_entry(self, updating_row: Optional[int] = None) -> BriefingEntry:
        if not self.title.text().strip():
            raise ValueError("Briefing Title cannot be blank!")
        return BriefingEntry(
            title=self.title.text(),
            description=self.description.toPlainText(),
        )

    def _load_entry(self, entry: BriefingEntry) -> None:
        self.title.setText(entry.title)
        self.description.setPlainText(entry.description)

    def _label(self, entry: BriefingEntry) -> str:
        return entry.title

    def apply(self, config: MissionConfig) -> None:
        config.briefings = list(self.entries)
