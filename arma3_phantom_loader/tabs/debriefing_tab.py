"""Tab 4: debriefing entries (CfgDebriefing / debriefing.hpp)."""
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import (QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPlainTextEdit, QPushButton, QVBoxLayout)

from ..model import DebriefEntry, MissionConfig
from .entry_list import EntryListTab


class DebriefingTab(EntryListTab):
    def _build_form(self, layout: QVBoxLayout) -> None:
        layout.addWidget(QLabel(
            "How the mission can end. Class names must be unique and alphanumeric\n"
            '(end the mission with e.g. ["Win", true, 2] call BIS_fnc_endMission;).'))

        presets = QHBoxLayout()
        win_button = QPushButton("Win preset")
        win_button.clicked.connect(self._preset_win)
        lose_button = QPushButton("Lose preset")
        lose_button.clicked.connect(self._preset_lose)
        presets.addWidget(win_button)
        presets.addWidget(lose_button)
        presets.addStretch()
        layout.addLayout(presets)

        form = QFormLayout()
        self.classname = QLineEdit()
        self.title = QLineEdit()
        self.subtitle = QLineEdit()
        self.description = QPlainTextEdit()
        self.description.setFixedHeight(80)
        self.picture_background = QLineEdit()
        self.picture_background.setPlaceholderText("images\\loadscreen.jpg")
        form.addRow("Class name", self.classname)
        form.addRow("Title", self.title)
        form.addRow("Subtitle", self.subtitle)
        form.addRow("Description", self.description)
        form.addRow("Picture background", self.picture_background)
        layout.addLayout(form)

    def _preset_win(self) -> None:
        self.classname.setText("Win")
        self.title.setText("Mission Accomplished")

    def _preset_lose(self) -> None:
        self.classname.setText("Lose")
        self.title.setText("Mission Failed")

    def _make_entry(self, updating_row: Optional[int] = None) -> DebriefEntry:
        name = self.classname.text().strip()
        if not name:
            raise ValueError("Please fill in a classname!")
        if not name.isalnum():
            raise ValueError("Classnames can only be alphanumeric.")
        for row, entry in enumerate(self.entries):
            if row != updating_row and entry.classname.lower() == name.lower():
                raise ValueError(f"{name} classname already exists! "
                                 "Please try a different name.")
        return DebriefEntry(
            classname=name,
            title=self.title.text(),
            subtitle=self.subtitle.text(),
            description=self.description.toPlainText(),
            picture_background=self.picture_background.text(),
        )

    def _load_entry(self, entry: DebriefEntry) -> None:
        self.classname.setText(entry.classname)
        self.title.setText(entry.title)
        self.subtitle.setText(entry.subtitle)
        self.description.setPlainText(entry.description)
        self.picture_background.setText(entry.picture_background)

    def _label(self, entry: DebriefEntry) -> str:
        return f"{entry.classname} — {entry.title}"

    def apply(self, config: MissionConfig) -> None:
        config.debriefings = list(self.entries)
