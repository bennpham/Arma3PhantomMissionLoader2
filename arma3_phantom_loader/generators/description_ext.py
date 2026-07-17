"""Generate description.ext."""
from __future__ import annotations

from pathlib import Path
from typing import List

from ..model import MissionConfig

DESCRIPTION = "description.ext"


def _esc(text: str) -> str:
    return text.replace('"', '""')


def _one_line(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\n", " ")


def write_description_ext(mission_dir: str, config: MissionConfig) -> Path:
    mission = config.mission
    desc = config.description

    lines: List[str] = [
        'overviewPicture = "images\\loadscreen.jpg";',
        f'author="{_esc(mission.author)}";',
        'loadScreen = "images\\loadscreen.jpg";',
        f'OnLoadName = "{_one_line(_esc(mission.on_load_name))}";',
        f'OnLoadMission ="{_one_line(_esc(mission.on_load_mission))}";',
        "debriefing = 1;",
        "",
        "allowFunctionsRecompile = 1;",
        "",
        "class Header",
        "{",
        "  gameType = Coop;",
        f"  minPlayers = {mission.min_players};",
        f"  maxPlayers = {mission.max_players};",
        "  playerCountMultipleOf = 1;",
        "};",
        "",
        'respawn = "SIDE";',
        "respawnDelay = 5;",
        "",
        "class CfgDebriefing",
        "{",
        '\t#include "debriefing.hpp"',
        "};",
        "",
    ]
    if config.taw_vd.enabled:
        lines.append('#include "functions\\taw_vd\\GUI.h"')
    lines += [
        "class CfgFunctions {",
        '\t#include "functions\\common.hpp"',
        "};",
    ]
    if desc.params_scale_players or desc.params_fhq_difficulty:
        lines += [
            "",
            "class Params",
            "{",
            '\t#include "scripts\\parameters.hpp"',
            "};",
        ]
    if desc.description_loadout:
        lines += [
            "",
            '#include "scripts\\briefing_loadout.hpp"',
        ]

    path = Path(mission_dir) / DESCRIPTION
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
