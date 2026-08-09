"""Generate init.sqf."""
from __future__ import annotations

from pathlib import Path
from typing import List

from ..model import MissionConfig
from . import sqf_blocks

INIT = "init.sqf"


def write_init_sqf(mission_dir: str, config: MissionConfig) -> Path:
    desc = config.description
    lines: List[str] = [
        "// Copy from FHQ missions init.sqf",
        "FHQ_allPlayableUnits = (if (isMultiplayer) then {playableUnits} else {switchableUnits});",
        "FHQ_startingUnits = allUnits + vehicles + allUnitsUAV;",
        "",
        "/* Filter out spectators and actual players, and player groups */",
        "FHQ_playableUnits = [];",
        "FHQ_playableGroups = [];",
        "{",
        "    if (side _x != sideLogic) then {",
        "        FHQ_playableUnits pushBack _x;",
        "",
        "        if (!((group _x) in FHQ_playableGroups)) then {",
        "           FHQ_playableGroups pushBack (group _x);",
        "        };",
        "    };",
        "} forEach FHQ_allPlayableUnits;",
        "",
        "/* When players die, they will be able to see all units, not just",
        " * players and their own side",
        " */",
        "{",
        '//\t_x setVariable ["WhitelistedSides", ["WEST", "EAST", "RESISTANCE", "CIVILIAN"]];',
        '\t_x setVariable ["AllowAI", true];',
        '//\t_x setVariable ["ShowControlsHelper", false];',
        '\t_x setVariable ["ShowFocusInfo", false];',
        "} forEach FHQ_playableUnits;",
        "",
        'publicVariable "FHQ_playableUnits";',
        "",
        "//=============================================================================================",
        "",
        'call compile preProcessFileLineNumbers "scripts\\briefing.sqf";',
    ]

    if desc.use_main_sqf:
        # The server-side setup lives in functions\pht6\main.sqf instead.
        lines.append("")
        lines.append("[] spawn PHT6_fnc_main;")

    if config.taw_vd.enabled:
        lines.append("")
        lines.append("// TAW View Distance settings")
        if config.taw_vd.disable_none:
            lines.append("tawvd_disablenone = true;")
        if config.taw_vd.enable_max_range:
            lines.append(f"tawvd_maxRange = {config.taw_vd.max_range};")

    if not desc.use_main_sqf:
        if desc.init_ace:
            lines += [""] + sqf_blocks.ace_block()
        if desc.params_scale_players:
            lines += [""] + sqf_blocks.scale_players_block()
        if desc.init_zeus:
            lines += [""] + sqf_blocks.zeus_block()
    lines.append("")
    if config.weather.enabled:
        lines.append('call compile preProcessFileLineNumbers "scripts\\weatherScript.sqf";')
    lines.append('call compile preProcessFileLineNumbers "scripts\\infotext.sqf";')

    path = Path(mission_dir) / INIT
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
