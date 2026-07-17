"""Tab 6: briefing tasks loaded by FHQ TaskTracker (FHQ_fnc_ttAddTasks)."""
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import (QComboBox, QFormLayout, QLabel, QLineEdit,
                               QPlainTextEdit, QVBoxLayout)

from ..model import TASK_STATES, TASK_TYPES, MissionConfig, TaskEntry
from .entry_list import EntryListTab
from .markup_helpers import MarkupHelperBox


class TasksTab(EntryListTab):
    def _build_form(self, layout: QVBoxLayout) -> None:
        layout.addWidget(QLabel(
            "Task names must be unique (task1, task2, … taskN recommended).\n"
            "Only one task may start in the 'assigned' state."))
        form = QFormLayout()
        self.name = QLineEdit()
        self.title = QLineEdit()
        self.description = QPlainTextEdit()
        self.description.setFixedHeight(80)
        self.waypoint_text = QLineEdit()
        self.marker = QLineEdit()
        self.state = QComboBox()
        self.state.addItems(TASK_STATES)
        self.task_type = QComboBox()
        self.task_type.addItems(TASK_TYPES)
        form.addRow("Task name", self.name)
        form.addRow("Task title", self.title)
        form.addRow("Description", self.description)
        form.addRow("Waypoint text", self.waypoint_text)
        form.addRow("Marker name (position)", self.marker)
        form.addRow("Initial state", self.state)
        form.addRow("Task type", self.task_type)
        layout.addLayout(form)
        layout.addWidget(MarkupHelperBox(self.description))

    def _make_entry(self, updating_row: Optional[int] = None) -> TaskEntry:
        name = self.name.text().strip()
        if not name:
            raise ValueError("Task Name cannot be blank!")
        if "'" in name or '"' in name:
            raise ValueError("Task name must not contain any quotes.")
        if not self.title.text().strip():
            raise ValueError("Task Title cannot be blank!")
        marker = self.marker.text()
        if "'" in marker or '"' in marker:
            raise ValueError("Task Marker Name must not contain any quotes.")
        for row, entry in enumerate(self.entries):
            if row != updating_row and entry.name.lower() == name.lower():
                raise ValueError(f"{name} has already been defined!")
        if self.state.currentText() == "assigned":
            for row, entry in enumerate(self.entries):
                if row != updating_row and entry.state == "assigned":
                    raise ValueError("Only 1 task state can start off as Assigned!")
        return TaskEntry(
            name=name,
            title=self.title.text(),
            description=self.description.toPlainText(),
            waypoint_text=self.waypoint_text.text(),
            marker=marker,
            state=self.state.currentText(),
            task_type=self.task_type.currentText(),
        )

    def _load_entry(self, entry: TaskEntry) -> None:
        self.name.setText(entry.name)
        self.title.setText(entry.title)
        self.description.setPlainText(entry.description)
        self.waypoint_text.setText(entry.waypoint_text)
        self.marker.setText(entry.marker)
        self.state.setCurrentText(entry.state)
        self.task_type.setCurrentText(entry.task_type)

    def _label(self, entry: TaskEntry) -> str:
        return f"{entry.name} — {entry.title}"

    def apply(self, config: MissionConfig) -> None:
        config.tasks = list(self.entries)
