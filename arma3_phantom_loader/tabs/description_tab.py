"""Tab 2: description.ext parameters, init.sqf extras and the infotext."""
from __future__ import annotations

from PySide6.QtWidgets import (QCheckBox, QGroupBox, QLabel, QPlainTextEdit,
                               QVBoxLayout, QWidget)

from ..model import MissionConfig


class DescriptionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        params_box = QGroupBox("Description parameters (require manual setup — see SETUP.md)")
        params_layout = QVBoxLayout(params_box)
        self.params_scale_players = QCheckBox(
            "Description Params (Player Count Scale) — in-game parameter to scale units")
        self.params_fhq_difficulty = QCheckBox(
            "Description Params (FHQ Difficulty) — delete units based on MP difficulty")
        self.description_loadout = QCheckBox(
            "Description Loadout (Singleplayer only) — scripts/briefing_loadout.hpp")
        params_layout.addWidget(self.params_scale_players)
        params_layout.addWidget(self.params_fhq_difficulty)
        params_layout.addWidget(self.description_loadout)
        layout.addWidget(params_box)

        init_box = QGroupBox("init.sqf extras")
        init_layout = QVBoxLayout(init_box)
        self.init_ace = QCheckBox(
            "Init ACE Extra — add extra ACE equipment block (fill in the TODO)")
        self.init_zeus = QCheckBox(
            "Init Zeus — make all editor-placed units controllable by zeus_mod1-3")
        init_layout.addWidget(self.init_ace)
        init_layout.addWidget(self.init_zeus)
        layout.addWidget(init_box)

        infotext_box = QGroupBox("Info text")
        infotext_layout = QVBoxLayout(infotext_box)
        infotext_layout.addWidget(QLabel(
            "Shown on mission start between the date/time and the author line.\n"
            "Each line becomes its own infotext line."))
        self.infotext = QPlainTextEdit()
        infotext_layout.addWidget(self.infotext)
        layout.addWidget(infotext_box)

        layout.addStretch()

    def apply(self, config: MissionConfig) -> None:
        desc = config.description
        desc.params_scale_players = self.params_scale_players.isChecked()
        desc.params_fhq_difficulty = self.params_fhq_difficulty.isChecked()
        desc.description_loadout = self.description_loadout.isChecked()
        desc.init_ace = self.init_ace.isChecked()
        desc.init_zeus = self.init_zeus.isChecked()
        desc.infotext = self.infotext.toPlainText()
