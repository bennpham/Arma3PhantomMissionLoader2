"""Tab 1: mission folder + everything written into mission.sqm."""
from __future__ import annotations

from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (QCheckBox, QDateEdit, QFileDialog, QFormLayout,
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QPlainTextEdit, QPushButton,
                               QScrollArea, QSpinBox, QVBoxLayout, QWidget)

from ..model import MissionConfig


def _spin(minimum: int, maximum: int, value: int) -> QSpinBox:
    box = QSpinBox()
    box.setRange(minimum, maximum)
    box.setValue(value)
    return box


class MissionTab(QScrollArea):
    # Emitted with the mission folder path whenever it changes, so the marker
    # pickers in other tabs can re-parse mission.sqm.
    folder_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        content = QWidget()
        layout = QVBoxLayout(content)

        # ----------------------------------------------------- mission folder
        folder_box = QGroupBox("Mission folder (must contain an unbinarized mission.sqm)")
        folder_layout = QHBoxLayout(folder_box)
        self.folder_edit = QLineEdit()
        self.folder_edit.setPlaceholderText("Path to your mission folder…")
        self.folder_edit.editingFinished.connect(self._folder_changed)
        browse = QPushButton("Browse…")
        browse.clicked.connect(self._browse)
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(browse)
        layout.addWidget(folder_box)

        # ------------------------------------------------------- mission info
        info_box = QGroupBox("Mission information")
        info_form = QFormLayout(info_box)
        self.author = QLineEdit()
        self.on_load_name = QLineEdit()
        self.on_load_mission = QLineEdit()
        self.overview_text = QPlainTextEdit()
        self.overview_text.setFixedHeight(70)
        self.summary = QPlainTextEdit()
        self.summary.setFixedHeight(70)
        info_form.addRow("Author", self.author)
        info_form.addRow("Mission name (OnLoadName)", self.on_load_name)
        info_form.addRow("Loading text (OnLoadMission)", self.on_load_mission)
        info_form.addRow("Overview text", self.overview_text)
        info_form.addRow("Mission summary (briefing Intel)", self.summary)
        layout.addWidget(info_box)

        # -------------------------------------------------------- date & time
        datetime_box = QGroupBox("Mission date && start time")
        datetime_layout = QHBoxLayout(datetime_box)
        self.date = QDateEdit(QDate(2035, 6, 24))
        self.date.setCalendarPopup(True)
        self.hour = _spin(0, 23, 12)
        self.minute = _spin(0, 59, 0)
        datetime_layout.addWidget(QLabel("Date"))
        datetime_layout.addWidget(self.date)
        datetime_layout.addWidget(QLabel("Hour"))
        datetime_layout.addWidget(self.hour)
        datetime_layout.addWidget(QLabel("Minute"))
        datetime_layout.addWidget(self.minute)
        datetime_layout.addStretch()
        layout.addWidget(datetime_box)

        # -------------------------------------------------------- multiplayer
        mp_box = QGroupBox("Multiplayer")
        mp_grid = QGridLayout(mp_box)
        self.min_players = _spin(1, 999, 1)
        self.max_players = _spin(1, 999, 16)
        self.allow_ai_score = QCheckBox("Allow AI kills to score")
        self.enable_team_switch = QCheckBox("Enable team switch")
        self.enable_team_switch.setChecked(True)
        self.manual_respawn = QCheckBox("Allow manual respawn button")
        self.mp_mission_fail = QCheckBox("Mission fails when everyone is dead (EndMission)")
        self.mp_mission_fail.setChecked(True)
        self.mp_sp_death_screen = QCheckBox("Singleplayer death screen (None)")
        self.mp_sp_death_screen.setChecked(True)
        self.mp_switch_char = QCheckBox("Switch to another unit on death (SwitchPlayer)")
        mp_grid.addWidget(QLabel("Min players"), 0, 0)
        mp_grid.addWidget(self.min_players, 0, 1)
        mp_grid.addWidget(QLabel("Max players"), 0, 2)
        mp_grid.addWidget(self.max_players, 0, 3)
        mp_grid.addWidget(self.allow_ai_score, 1, 0, 1, 2)
        mp_grid.addWidget(self.enable_team_switch, 1, 2, 1, 2)
        mp_grid.addWidget(self.manual_respawn, 2, 0, 1, 2)
        mp_grid.addWidget(self.mp_mission_fail, 2, 2, 1, 2)
        mp_grid.addWidget(self.mp_sp_death_screen, 3, 0, 1, 2)
        mp_grid.addWidget(self.mp_switch_char, 3, 2, 1, 2)
        layout.addWidget(mp_box)

        # -------------------------------------------------------------- intel
        intel_box = QGroupBox("Intel")
        intel_grid = QGridLayout(intel_box)
        self.resistance_west = QCheckBox("Independents allied with BLUFOR")
        self.resistance_west.setChecked(True)
        self.resistance_east = QCheckBox("Independents allied with OPFOR")
        intel_grid.addWidget(self.resistance_west, 0, 0, 1, 3)
        intel_grid.addWidget(self.resistance_east, 0, 3, 1, 3)
        self.toc_hours = _spin(0, 8, 0)
        self.toc_minutes = _spin(0, 59, 0)
        self.toc_seconds = _spin(0, 59, 0)
        intel_grid.addWidget(QLabel("Time of changes (max 8h)"), 1, 0)
        intel_grid.addWidget(self.toc_hours, 1, 1)
        intel_grid.addWidget(QLabel("h"), 1, 2)
        intel_grid.addWidget(self.toc_minutes, 1, 3)
        intel_grid.addWidget(QLabel("m"), 1, 4)
        intel_grid.addWidget(self.toc_seconds, 1, 5)
        layout.addWidget(intel_box)

        # ------------------------------------------------------------ weather
        weather_box = QGroupBox("Weather (0–100)")
        weather_grid = QGridLayout(weather_box)
        self.overcast_start = _spin(0, 100, 0)
        self.overcast_forecast = _spin(0, 100, 0)
        self.fog_start = _spin(0, 100, 0)
        self.fog_forecast = _spin(0, 100, 0)
        self.fog_start_base = _spin(0, 5000, 0)
        self.fog_forecast_base = _spin(0, 5000, 0)
        self.fog_start_decay = _spin(0, 100, 0)
        self.fog_forecast_decay = _spin(0, 100, 0)
        rows = [
            ("Overcast start", self.overcast_start, "Overcast forecast", self.overcast_forecast),
            ("Fog start", self.fog_start, "Fog forecast", self.fog_forecast),
            ("Fog base start (m)", self.fog_start_base, "Fog base forecast (m)", self.fog_forecast_base),
            ("Fog decay start", self.fog_start_decay, "Fog decay forecast", self.fog_forecast_decay),
        ]
        for row, (label1, widget1, label2, widget2) in enumerate(rows):
            weather_grid.addWidget(QLabel(label1), row, 0)
            weather_grid.addWidget(widget1, row, 1)
            weather_grid.addWidget(QLabel(label2), row, 2)
            weather_grid.addWidget(widget2, row, 3)
        layout.addWidget(weather_box)

        layout.addStretch()
        self.setWidget(content)
        self.setWidgetResizable(True)

    def _browse(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select mission folder")
        if folder:
            self.folder_edit.setText(folder)
            self._folder_changed()

    def _folder_changed(self) -> None:
        self.folder_changed.emit(self.folder_edit.text().strip())

    def apply(self, config: MissionConfig) -> None:
        config.mission_dir = self.folder_edit.text().strip()
        mission = config.mission
        mission.author = self.author.text()
        mission.on_load_name = self.on_load_name.text()
        mission.on_load_mission = self.on_load_mission.text()
        mission.overview_text = self.overview_text.toPlainText()
        mission.summary = self.summary.toPlainText()
        date = self.date.date()
        mission.year, mission.month, mission.day = date.year(), date.month(), date.day()
        mission.hour = self.hour.value()
        mission.minute = self.minute.value()
        mission.min_players = self.min_players.value()
        mission.max_players = self.max_players.value()
        mission.allow_ai_score = self.allow_ai_score.isChecked()
        mission.enable_team_switch = self.enable_team_switch.isChecked()
        mission.manual_respawn = self.manual_respawn.isChecked()
        mission.mp_mission_fail = self.mp_mission_fail.isChecked()
        mission.mp_sp_death_screen = self.mp_sp_death_screen.isChecked()
        mission.mp_switch_char = self.mp_switch_char.isChecked()
        mission.resistance_west = self.resistance_west.isChecked()
        mission.resistance_east = self.resistance_east.isChecked()
        mission.toc_hours = self.toc_hours.value()
        mission.toc_minutes = self.toc_minutes.value()
        mission.toc_seconds = self.toc_seconds.value()
        mission.overcast_start = self.overcast_start.value()
        mission.overcast_forecast = self.overcast_forecast.value()
        mission.fog_start = self.fog_start.value()
        mission.fog_forecast = self.fog_forecast.value()
        mission.fog_start_base = self.fog_start_base.value()
        mission.fog_forecast_base = self.fog_forecast_base.value()
        mission.fog_start_decay = self.fog_start_decay.value()
        mission.fog_forecast_decay = self.fog_forecast_decay.value()
