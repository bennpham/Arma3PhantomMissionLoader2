"""Tab 3: optional scripts. All FHQ functions (fhq_ai, fhq_misc,
fhq_tasktracker) are always installed; only TAW View Distance and the
weather-effects FSM are opt-in."""
from __future__ import annotations

from PySide6.QtWidgets import (QCheckBox, QGridLayout, QGroupBox, QLabel,
                               QSpinBox, QVBoxLayout, QWidget)

from ..model import MissionConfig


class ScriptsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(
            "FHQ TaskTracker, FHQ AI and FHQ Misc functions are always installed.\n"
            "Extra setup for some of them is described in SETUP.md."))

        # ------------------------------------------------- TAW View Distance
        self.taw_box = QGroupBox("TAW View Distance")
        self.taw_box.setCheckable(True)
        self.taw_box.setChecked(False)
        taw_grid = QGridLayout(self.taw_box)
        self.taw_disable_none = QCheckBox('Disable the "no grass" option for players')
        self.taw_enable_max_range = QCheckBox("Limit max view distance")
        self.taw_max_range = QSpinBox()
        self.taw_max_range.setRange(500, 20000)
        self.taw_max_range.setValue(10000)
        self.taw_max_range.setSuffix(" m")
        taw_grid.addWidget(self.taw_disable_none, 0, 0, 1, 2)
        taw_grid.addWidget(self.taw_enable_max_range, 1, 0)
        taw_grid.addWidget(self.taw_max_range, 1, 1)
        layout.addWidget(self.taw_box)

        # ------------------------------------------------- FHQ Weather Effect
        self.weather_box = QGroupBox(
            "FHQ Weather Effects (copies functions/weatherEffects.fsm)")
        self.weather_box.setCheckable(True)
        self.weather_box.setChecked(False)
        weather_grid = QGridLayout(self.weather_box)
        weather_grid.addWidget(QLabel(
            "Interval = seconds between effect loops — lower is stronger."), 0, 0, 1, 4)
        self.weather_effects = {}
        for row, name in enumerate(["fog", "sand", "snow", "wind"], start=1):
            checkbox = QCheckBox(name.capitalize())
            interval = QSpinBox()
            interval.setRange(1, 3600)
            interval.setValue(10)
            interval.setSuffix(" s")
            weather_grid.addWidget(checkbox, row, 0)
            weather_grid.addWidget(QLabel("Interval"), row, 1)
            weather_grid.addWidget(interval, row, 2)
            self.weather_effects[name] = (checkbox, interval)
        layout.addWidget(self.weather_box)

        layout.addStretch()

    def apply(self, config: MissionConfig) -> None:
        taw = config.taw_vd
        taw.enabled = self.taw_box.isChecked()
        taw.disable_none = self.taw_disable_none.isChecked()
        taw.enable_max_range = self.taw_enable_max_range.isChecked()
        taw.max_range = self.taw_max_range.value()

        weather = config.weather
        weather.enabled = self.weather_box.isChecked()
        for name in ["fog", "sand", "snow", "wind"]:
            checkbox, interval = self.weather_effects[name]
            setattr(weather, name, checkbox.isChecked())
            setattr(weather, f"{name}_interval", interval.value())
