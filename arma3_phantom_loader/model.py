"""Dataclasses holding every setting collected by the GUI.

The GUI tabs only read/write these; all file generation lives in
arma3_phantom_loader.generators so the pipeline is testable without Qt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

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
    description: str = ""
    title: str = ""
    waypoint_text: str = ""
    marker: str = ""
    state: str = "created"
    task_type: str = ""


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
            if task.state == "assigned":
                assigned += 1
        if assigned > 1:
            problems.append("Only one task may start in the 'assigned' state.")
        for entry in self.briefings:
            if not entry.title.strip():
                problems.append("A briefing entry has an empty title.")
        return problems
