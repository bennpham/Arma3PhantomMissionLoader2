"""Install the SQF functions payload into the mission and write common.hpp.

All FHQ files (fhq_ai, fhq_misc, fhq_tasktracker) are mandatory and always
included in common.hpp. taw_vd is copied/included only when TAW View Distance
is enabled, and weatherEffects.fsm only when weather effects are enabled.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import List

from ..model import MissionConfig

FOLDER_FUNCTIONS = "functions"
COMMON_HPP = "common.hpp"

FHQ_MANDATORY_FOLDERS = ["fhq_ai", "fhq_misc", "fhq_tasktracker"]
FHQ_MANDATORY_HPPS = ["fhq_ai.hpp", "fhq_misc.hpp", "fhq_tasktracker.hpp"]
TAW_VD_FOLDER = "taw_vd"
WEATHER_FSM = "weatherEffects.fsm"

COMMON_HPP_MACROS = '''#define INTERNAL_FUNCTION(x)\t\t\t\t\\
\tclass x\t\t\t\t\t\t\t\t\t\\
\t{\t\t\t\t\t\t\t\t\t\t\\
\t\tdescription = "Internal Function";\t\\
\t};

#define EXPORTED_FUNCTION(x,y)\t\t\t\t\\
\tclass x\t\t\t\t\t\t\t\t\t\\
\t{\t\t\t\t\t\t\t\t\t\t\\
\t\tdescription = y;\t\t\t\t\t\\
\t};
'''

PHT6_CLASS = '''class PHT6
{
\tclass phantomsix_insurgentFunctions {
\t\tclass main {file = "functions\\pht6\\main.sqf";};
\t};
};
'''


def install_functions(mission_dir: str, config: MissionConfig,
                      payload_functions: Path) -> List[Path]:
    """Copy the payload into <mission>/functions and generate common.hpp."""
    written: List[Path] = []
    dest = Path(mission_dir) / FOLDER_FUNCTIONS
    dest.mkdir(parents=True, exist_ok=True)

    for folder in FHQ_MANDATORY_FOLDERS:
        shutil.copytree(payload_functions / folder, dest / folder, dirs_exist_ok=True)
        written.append(dest / folder)
    for hpp in FHQ_MANDATORY_HPPS:
        shutil.copy2(payload_functions / hpp, dest / hpp)
        written.append(dest / hpp)

    if config.taw_vd.enabled:
        shutil.copytree(payload_functions / TAW_VD_FOLDER, dest / TAW_VD_FOLDER,
                        dirs_exist_ok=True)
        written.append(dest / TAW_VD_FOLDER)

    if config.weather.enabled:
        shutil.copy2(payload_functions / WEATHER_FSM, dest / WEATHER_FSM)
        written.append(dest / WEATHER_FSM)

    common = dest / COMMON_HPP
    common.write_text(build_common_hpp(config), encoding="utf-8")
    written.append(common)
    return written


def build_common_hpp(config: MissionConfig) -> str:
    parts = [COMMON_HPP_MACROS]
    if config.taw_vd.enabled:
        parts.append('#include "taw_vd\\CfgFunctions.hpp"\n')
    parts.append("class FHQ\n{")
    parts.append('\t#include "fhq_ai.hpp"')
    parts.append('\t#include "fhq_misc.hpp"')
    parts.append('\t#include "fhq_tasktracker.hpp"')
    parts.append("};\n")
    if config.description.use_main_sqf:
        parts.append(PHT6_CLASS)
    return "\n".join(parts)
