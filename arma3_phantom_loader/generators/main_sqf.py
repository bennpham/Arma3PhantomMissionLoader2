"""Generate functions\\pht6\\main.sqf (PHT6_fnc_main).

Only written when the "Use main.sqf" option is on. The file is never
overwritten: mission makers hand-edit it heavily (randomization, spawn
handles), so an existing main.sqf is left alone on a re-run.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from ..model import MissionConfig
from . import sqf_blocks

FOLDER_FUNCTIONS = "functions"
PHT6_FOLDER = "pht6"
MAIN = "main.sqf"


def build_main_sqf(config: MissionConfig) -> str:
    desc = config.description
    body: List[str] = []
    if desc.init_ace:
        body += [""] + sqf_blocks.ace_block()
    if desc.params_scale_players:
        body += [""] + sqf_blocks.scale_players_block()
    if desc.init_zeus:
        body += [""] + sqf_blocks.zeus_block()
    if not body:
        body = ["", "// TODO"]

    lines = [
        "// Runs on the server once the mission has actually started, so every",
        "// editor-placed unit exists. Put randomization and unit scaling here.",
        "if (isServer) then {",
        "\twaitUntil { time > 0 };",
    ]
    lines += sqf_blocks.indent(body)
    lines.append("};")
    return "\n".join(lines) + "\n"


def write_main_sqf(mission_dir: str, config: MissionConfig) -> Optional[Path]:
    if not config.description.use_main_sqf:
        return None

    folder = Path(mission_dir) / FOLDER_FUNCTIONS / PHT6_FOLDER
    path = folder / MAIN
    if path.exists():
        return None

    folder.mkdir(parents=True, exist_ok=True)
    path.write_text(build_main_sqf(config), encoding="utf-8")
    return path
