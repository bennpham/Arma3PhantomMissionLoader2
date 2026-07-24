"""Dataclasses holding every setting collected by the GUI.

The GUI tabs only read/write these; all file generation lives in
arma3_phantom_loader.generators so the pipeline is testable without Qt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

TASK_STATES = ["created", "assigned", "succeeded", "failed", "canceled"]
# Source of truth for Task Types: https://community.bistudio.com/wiki/Arma_3:_Task_Framework#Task_Icons
# Grouped exactly as the wiki groups them (Actions, Objects, Letters), each
# alphabetical. "" means "leave the task type unset".
TASK_TYPE_ACTIONS = [
    "airdrop", "attack", "danger", "default", "defend", "destroy", "download",
    "exit", "getin", "getout", "heal", "interact", "kill", "land", "listen",
    "meet", "move", "move1", "move2", "move3", "move4", "move5", "navigate",
    "rearm", "refuel", "repair", "run", "scout", "search", "takeoff", "talk",
    "talk1", "talk2", "talk3", "talk4", "talk5", "target", "unknown", "upload",
    "use", "wait", "walk",
]
TASK_TYPE_OBJECTS = [
    "armor", "backpack", "boat", "box", "car", "container", "documents",
    "heli", "intel", "map", "mine", "plane", "radio", "rifle", "truck",
    "whiteboard",
]
# Full set of capital letter icons, named simply "a" .. "z".
TASK_TYPE_LETTERS = [chr(code) for code in range(ord("a"), ord("z") + 1)]

# (group label, types) in the order they are offered in the UI.
TASK_TYPE_GROUPS = [
    ("Actions", TASK_TYPE_ACTIONS),
    ("Objects", TASK_TYPE_OBJECTS),
    ("Letters", TASK_TYPE_LETTERS),
]
TASK_TYPES = [""] + [t for _, types in TASK_TYPE_GROUPS for t in types]


@dataclass
class MissionSettings:
    """Everything written into mission.sqm (plus shared description info)."""
    author: str = ""
    on_load_name: str = ""
    on_load_mission: str = ""
    overview_text: str = ""
    summary: str = ""
    # Date/time of the mission start (Intel)
    year: int = 2035
    month: int = 6
    day: int = 24
    hour: int = 12
    minute: int = 0
    # Multiplayer header
    min_players: int = 1
    max_players: int = 16
    # Multiplayer checkboxes
    allow_ai_score: bool = False
    enable_team_switch: bool = True
    manual_respawn: bool = False
    mp_mission_fail: bool = True
    mp_sp_death_screen: bool = True
    mp_switch_char: bool = False
    # Intel: resistance
    resistance_west: bool = True
    resistance_east: bool = False
    # Intel: time of changes (capped at 28800 seconds)
    toc_hours: int = 0
    toc_minutes: int = 0
    toc_seconds: int = 0
    # Intel: weather (0-100 as shown in the UI, divided by 100 in mission.sqm)
    overcast_start: int = 0
    overcast_forecast: int = 0
    fog_start: int = 0
    fog_forecast: int = 0
    fog_start_base: int = 0
    fog_forecast_base: int = 0
    fog_start_decay: int = 0
    fog_forecast_decay: int = 0


@dataclass
class DescriptionSettings:
    """Description.ext / init.sqf options plus the infotext."""
    params_scale_players: bool = False
    params_fhq_difficulty: bool = False
    description_loadout: bool = False
    init_ace: bool = False
    init_zeus: bool = False
    infotext: str = ""


@dataclass
class TawViewDistanceSettings:
    enabled: bool = False
    disable_none: bool = False
    enable_max_range: bool = False
    max_range: int = 10000


@dataclass
class WeatherEffectSettings:
    enabled: bool = False
    fog: bool = False
    fog_interval: int = 10
    sand: bool = False
    sand_interval: int = 10
    snow: bool = False
    snow_interval: int = 10
    wind: bool = False
    wind_interval: int = 10


@dataclass
class DebriefEntry:
    classname: str = ""
    title: str = ""
    subtitle: str = ""
    description: str = ""
    picture_background: str = ""


@dataclass
class BriefingEntry:
    title: str = ""
    description: str = ""


@dataclass
class TaskEntry:
    name: str = ""
    # Name of the task this one is a subtask of ("" for a top level task).
    parent: str = ""
    description: str = ""
    title: str = ""
    waypoint_text: str = ""
    marker: str = ""
    state: str = "created"
    task_type: str = ""


def ordered_tasks(tasks: List[TaskEntry]) -> List[Tuple[TaskEntry, int]]:
    """Return (task, depth) pairs, every parent placed before its children.

    FHQ_fnc_ttAddTasks creates the tasks in array order and resolves a subtask's
    parent by name (fn_ttiCreateOrUpdateTask), so a child written before its
    parent would be handed a nil parent. Tasks whose parent is empty or unknown
    count as top level; anything left over (a parent loop) is appended at the
    end so no task is ever dropped.
    """
    children: dict = {}
    roots: List[TaskEntry] = []
    names = {task.name for task in tasks}
    for task in tasks:
        if task.parent and task.parent != task.name and task.parent in names:
            children.setdefault(task.parent, []).append(task)
        else:
            roots.append(task)

    ordered: List[Tuple[TaskEntry, int]] = []
    seen = set()

    def walk(task: TaskEntry, depth: int) -> None:
        if id(task) in seen:
            return
        seen.add(id(task))
        ordered.append((task, depth))
        for child in children.get(task.name, []):
            walk(child, depth + 1)

    for task in roots:
        walk(task, 0)
    for task in tasks:  # tasks caught in a loop
        if id(task) not in seen:
            seen.add(id(task))
            ordered.append((task, 0))
    return ordered


@dataclass
class MissionConfig:
    mission_dir: str = ""
    mission: MissionSettings = field(default_factory=MissionSettings)
    description: DescriptionSettings = field(default_factory=DescriptionSettings)
    taw_vd: TawViewDistanceSettings = field(default_factory=TawViewDistanceSettings)
    weather: WeatherEffectSettings = field(default_factory=WeatherEffectSettings)
    debriefings: List[DebriefEntry] = field(default_factory=list)
    briefings: List[BriefingEntry] = field(default_factory=list)
    tasks: List[TaskEntry] = field(default_factory=list)

    def _looping_tasks(self) -> List[str]:
        """Names of tasks whose parent chain leads back to themselves.

        A self-parent is reported separately, so it is skipped here.
        """
        by_name = {task.name: task for task in self.tasks}
        looping = []
        for task in self.tasks:
            if not task.parent or task.parent == task.name:
                continue
            walked = {task.name}
            current = by_name.get(task.parent)
            while current is not None:
                if current.name == task.name:
                    looping.append(task.name)
                    break
                if current.name in walked:
                    break
                walked.add(current.name)
                current = by_name.get(current.parent) if current.parent else None
        return looping

    def validate(self) -> List[str]:
        """Return a list of validation problems (empty when good to generate)."""
        problems = []
        if not self.mission_dir:
            problems.append("No mission folder selected.")
        if not self.debriefings:
            problems.append("Please add at least one debriefing entry (e.g. Win / Lose).")
        seen = set()
        for entry in self.debriefings:
            name = entry.classname.strip()
            if not name:
                problems.append("A debriefing entry has an empty classname.")
            elif not name.isalnum():
                problems.append(f"Debriefing classname '{name}' must be alphanumeric.")
            elif name.lower() in seen:
                problems.append(f"Duplicate debriefing classname '{name}'.")
            seen.add(name.lower())
        seen = set()
        assigned = 0
        task_names = {task.name for task in self.tasks}
        for task in self.tasks:
            name = task.name.strip()
            if not name:
                problems.append("A task entry has an empty task name.")
            elif "'" in name or '"' in name:
                problems.append(f"Task name '{name}' must not contain quotes.")
            elif name.lower() in seen:
                problems.append(f"Duplicate task name '{name}'.")
            seen.add(name.lower())
            if not task.title.strip():
                problems.append(f"Task '{name}' has an empty title.")
            if "'" in task.marker or '"' in task.marker:
                problems.append(f"Task '{name}' marker must not contain quotes.")
            if task.parent:
                if task.parent == task.name:
                    problems.append(f"Task '{name}' cannot be its own parent.")
                elif task.parent not in task_names:
                    problems.append(
                        f"Task '{name}' has an unknown parent task '{task.parent}'.")
            if task.state == "assigned":
                assigned += 1
        if assigned > 1:
            problems.append("Only one task may start in the 'assigned' state.")
        for task in self._looping_tasks():
            problems.append(f"Task '{task}' is part of a parent/child loop.")
        for entry in self.briefings:
            if not entry.title.strip():
                problems.append("A briefing entry has an empty title.")
        return problems
