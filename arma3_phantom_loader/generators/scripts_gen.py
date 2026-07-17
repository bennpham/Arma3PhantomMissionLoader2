"""Generate the scripts/ folder: infotext.sqf, parameters.hpp,
briefing_loadout.hpp and weatherScript.sqf."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from ..model import DescriptionSettings, MissionConfig, WeatherEffectSettings

FOLDER_SCRIPTS = "scripts"
INFOTEXT = "infotext.sqf"
PARAMETERS = "parameters.hpp"
BRIEFING_LOADOUT = "briefing_loadout.hpp"
WEATHER_SCRIPT = "weatherScript.sqf"

MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


def _esc(text: str) -> str:
    return text.replace('"', '""')


def _scripts_dir(mission_dir: str) -> Path:
    path = Path(mission_dir) / FOLDER_SCRIPTS
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_infotext(mission_dir: str, config: MissionConfig) -> Path:
    """Info text shown on mission start: date/time, custom lines, author."""
    mission = config.mission
    date_text = f"{MONTH_NAMES[mission.month - 1]} {mission.day}, {mission.year}"
    time_text = f"{mission.hour:02d}:{mission.minute:02d}:00"
    titles = [line for line in
              config.description.infotext.replace("\r\n", "\n").split("\n")]
    title_array = "[" + ", ".join(f'"{_esc(t)}"' for t in titles) + "]"

    lines = [
        'waitUntil{!(isNil "BIS_fnc_init")};',
        "sleep 15;",
        f'\t["{date_text}", "{time_text}"] call BIS_fnc_infoText;',
        "sleep 3;",
        f"\t{title_array} call BIS_fnc_infoText;",
        "sleep 3;",
        f'\t["Created by","{_esc(mission.author)}"] call BIS_fnc_infoText;',
    ]
    path = _scripts_dir(mission_dir) / INFOTEXT
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_parameters_hpp(mission_dir: str,
                         desc: DescriptionSettings) -> Optional[Path]:
    """In-game lobby parameters; written when either param option is on."""
    if not (desc.params_scale_players or desc.params_fhq_difficulty):
        return None
    lines: List[str] = []
    if desc.params_scale_players:
        lines += [
            "class ScalePlayers",
            "{",
            '\ttitle = "Low Player Count Scale Mode";',
            "\tvalues[] = {0, 1};",
            '\ttexts[] = {"Disable", "Enable"};',
            "\tdefault = 0;",
            "};",
        ]
    if desc.params_fhq_difficulty:
        lines += [
            "class FHQ_Difficulty",
            "{",
            '\ttitle = "Difficulty";',
            "\tvalues[] = {0, 1, 2};",
            '\ttexts[] = {"Easy", "Normal", "Hard"};',
            "\tdefault = 1;",
            "};",
        ]
    path = _scripts_dir(mission_dir) / PARAMETERS
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_briefing_loadout(mission_dir: str,
                           desc: DescriptionSettings) -> Optional[Path]:
    """Empty placeholder the mission maker fills in by hand (SP only)."""
    if not desc.description_loadout:
        return None
    path = _scripts_dir(mission_dir) / BRIEFING_LOADOUT
    path.write_text("", encoding="utf-8")
    return path


def write_weather_script(mission_dir: str,
                         weather: WeatherEffectSettings) -> Optional[Path]:
    """Client-side weather effects driven by FHQ_fnc_weatherEffect, which runs
    functions/weatherEffects.fsm under the hood."""
    if not weather.enabled:
        return None
    effects = []
    intervals = []
    for name, on, interval in [
        ("fog", weather.fog, weather.fog_interval),
        ("sand", weather.sand, weather.sand_interval),
        ("snow", weather.snow, weather.snow_interval),
        ("wind", weather.wind, weather.wind_interval),
    ]:
        if on:
            effects.append(f'            ["{name}", {{true}}]')
            intervals.append(
                f'    [_handle, "{name}Interval", {interval}] call FHQ_fnc_setWeatherEffect;')

    lines = [
        "if (hasInterface) then {",
        "    _handle = [",
        "        cameraOn,",
        "        [",
        ",\n".join(effects),
        "        ]",
        "    ] call FHQ_fnc_weatherEffect;",
        "    FHQ_weather = _handle;",
    ]
    lines += intervals
    lines.append("};")
    path = _scripts_dir(mission_dir) / WEATHER_SCRIPT
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
