"""Main window: one tab per configuration section plus the Generate button."""
from __future__ import annotations

from PySide6.QtWidgets import (QMainWindow, QMessageBox, QPushButton,
                               QTabWidget, QVBoxLayout, QWidget)

from .generators.sqm_markers import parse_marker_names
from .model import MissionConfig
from .pipeline import MissionFolderError, generate_mission
from .tabs.briefing_tab import BriefingTab
from .tabs.debriefing_tab import DebriefingTab
from .tabs.description_tab import DescriptionTab
from .tabs.mission_tab import MissionTab
from .tabs.scripts_tab import ScriptsTab
from .tabs.tasks_tab import TasksTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arma 3 Phantom Mission Loader 2")
        self.resize(900, 720)

        self.mission_tab = MissionTab()
        self.description_tab = DescriptionTab()
        self.scripts_tab = ScriptsTab()
        self.debriefing_tab = DebriefingTab()
        self.briefing_tab = BriefingTab()
        self.tasks_tab = TasksTab()

        self.mission_tab.folder_changed.connect(self._refresh_markers)

        tabs = QTabWidget()
        tabs.addTab(self.mission_tab, "Mission")
        tabs.addTab(self.description_tab, "Description && Init")
        tabs.addTab(self.scripts_tab, "Scripts")
        tabs.addTab(self.debriefing_tab, "Debriefing")
        tabs.addTab(self.briefing_tab, "Briefing")
        tabs.addTab(self.tasks_tab, "Tasks")

        generate_button = QPushButton("Generate Mission Files")
        generate_button.setMinimumHeight(40)
        generate_button.clicked.connect(self.generate)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(tabs)
        layout.addWidget(generate_button)
        self.setCentralWidget(central)

    def _refresh_markers(self, mission_dir: str) -> None:
        names = parse_marker_names(mission_dir) if mission_dir else []
        self.tasks_tab.set_markers(names)
        self.briefing_tab.set_markers(names)

    def collect_config(self) -> MissionConfig:
        config = MissionConfig()
        for tab in (self.mission_tab, self.description_tab, self.scripts_tab,
                    self.debriefing_tab, self.briefing_tab, self.tasks_tab):
            tab.apply(config)
        return config

    def generate(self) -> None:
        config = self.collect_config()
        problems = config.validate()
        if problems:
            QMessageBox.critical(self, "Cannot generate",
                                 "\n".join(f"• {p}" for p in problems))
            return
        try:
            written = generate_mission(config)
        except MissionFolderError as error:
            QMessageBox.critical(self, "Mission folder problem", str(error))
            return
        except OSError as error:
            QMessageBox.critical(self, "Generation failed", str(error))
            return
        QMessageBox.information(
            self, "Mission generated",
            "Mission files generated successfully!\n\n"
            "The original mission.sqm was backed up to mission.sqm.old.\n\n"
            "Files written:\n" + "\n".join(written) +
            "\n\nSee SETUP.md for scripts that need extra manual setup.")
