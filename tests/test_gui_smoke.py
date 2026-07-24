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
    window.mission_tab._folder_changed()  # normally fired on editingFinished
    window.mission_tab.author.setText("Smoke Tester")

    # Markers parsed from the fixture mission.sqm populate every marker picker.
    def combo_items(combo):
        return [combo.itemText(i) for i in range(combo.count())]

    assert combo_items(window.tasks_tab.marker) == ["objective", "start"]
    assert combo_items(window.tasks_tab.markup.marker_input) == ["objective", "start"]
    assert combo_items(window.briefing_tab.markup.marker_input) == ["objective", "start"]
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
    window.tasks_tab.name.setText("task1a")
    window.tasks_tab.title.setText("Curly")
    window.tasks_tab.parent_task.setCurrentText("task1")
    window.tasks_tab._add()
    assert [t.parent for t in window.tasks_tab.entries] == ["", "task1"]

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


def test_subtasks_are_nested_and_orphans_promoted(app, monkeypatch):
    from PySide6.QtWidgets import QMessageBox

    from arma3_phantom_loader.tabs.tasks_tab import TasksTab

    errors = []
    monkeypatch.setattr(QMessageBox, "critical",
                        lambda *a, **k: errors.append(a))

    tab = TasksTab()
    for name, title, parent in (("task2", "Exfil", ""),
                                ("task1", "Kill the officers", ""),
                                ("task1a", "Curly", "task1")):
        tab.name.setText(name)
        tab.title.setText(title)
        tab.parent_task.setCurrentText(parent)
        tab._add()
    assert not errors

    # The subtask is sorted under its parent and indented in the list.
    assert [t.name for t in tab.entries] == ["task2", "task1", "task1a"]
    rows = [tab.list_widget.item(i).text() for i in range(tab.list_widget.count())]
    assert rows[1] == "task1 — Kill the officers"
    assert rows[2] == "    ↳ task1a — Curly"

    # A task cannot be offered itself (or its own descendants) as a parent.
    tab.list_widget.setCurrentRow(1)
    offered = [tab.parent_task.itemText(i) for i in range(tab.parent_task.count())]
    assert offered == ["", "task2"]

    # Removing the parent promotes the subtask to a top level task.
    tab._remove()
    assert [(t.name, t.parent) for t in tab.entries] == [("task2", ""),
                                                         ("task1a", "")]
    assert tab.list_widget.item(1).text() == "task1a — Curly"


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
