"""Headless GUI smoke test: build the window, drive the tabs, generate."""
import os
import shutil
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")

FIXTURE = Path(__file__).parent / "fixtures" / "mission_folder"


@pytest.fixture(scope="module")
def app():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


def test_window_generates_mission(app, tmp_path, monkeypatch):
    from PySide6.QtWidgets import QMessageBox

    from arma3_phantom_loader.main_window import MainWindow

    mission_dir = tmp_path / "smoke.Altis"
    shutil.copytree(FIXTURE, mission_dir)

    window = MainWindow()
    window.mission_tab.folder_edit.setText(str(mission_dir))
    window.mission_tab.author.setText("Smoke Tester")
    window.description_tab.infotext.setPlainText("Smoke Run")
    window.scripts_tab.taw_box.setChecked(True)
    window.scripts_tab.weather_box.setChecked(True)
    window.scripts_tab.weather_effects["fog"][0].setChecked(True)

    # Debriefing entry via the tab's own Add flow
    window.debriefing_tab.classname.setText("Win")
    window.debriefing_tab.title.setText("Mission Accomplished")
    window.debriefing_tab._add()
    assert len(window.debriefing_tab.entries) == 1

    # Briefing + task
    window.briefing_tab.title.setText("Situation")
    window.briefing_tab.description.setPlainText("Enemy ahead")
    window.briefing_tab._add()
    window.tasks_tab.name.setText("task1")
    window.tasks_tab.title.setText("Clear town")
    window.tasks_tab._add()

    # Swallow the result dialogs
    infos, errors = [], []
    monkeypatch.setattr(QMessageBox, "information",
                        lambda *a, **k: infos.append(a))
    monkeypatch.setattr(QMessageBox, "critical",
                        lambda *a, **k: errors.append(a))

    window.generate()

    assert not errors, f"generate reported errors: {errors}"
    assert infos, "expected a success dialog"
    assert (mission_dir / "description.ext").is_file()
    assert (mission_dir / "init.sqf").is_file()
    assert (mission_dir / "functions" / "taw_vd").is_dir()
    assert (mission_dir / "functions" / "weatherEffects.fsm").is_file()
    assert (mission_dir / "mission.sqm.old").is_file()


def test_duplicate_debriefing_rejected(app, monkeypatch):
    from PySide6.QtWidgets import QMessageBox

    from arma3_phantom_loader.tabs.debriefing_tab import DebriefingTab

    errors = []
    monkeypatch.setattr(QMessageBox, "critical",
                        lambda *a, **k: errors.append(a))

    tab = DebriefingTab()
    tab.classname.setText("Win")
    tab.title.setText("Mission Accomplished")
    tab._add()
    tab._add()  # duplicate classname must be rejected
    assert len(tab.entries) == 1
    assert errors
