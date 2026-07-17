"""Dataclasses holding every setting collected by the GUI.

The GUI tabs only read/write these; all file generation lives in
arma3_phantom_loader.generators so the pipeline is testable without Qt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

TASK_STATES = ["created", "assigned", "succeeded", "failed", "cancelled"]
TASK_TYPES = [
    "", "attack", "defend", "destroy", "move", "getin", "getout",
    "search", "talk", "target", "meet", "navigate", "repair",
    "rearm", "refuel", "heal", "takeoff", "land", "scout",
]


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
