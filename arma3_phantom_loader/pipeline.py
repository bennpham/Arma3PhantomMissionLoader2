"""Run the full mission generation from a validated MissionConfig."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import List

from . import payload
from .model import MissionConfig
from .generators import (briefing_gen, debriefing_gen, description_ext,
                         functions_payload, init_sqf, scripts_gen, sqm_editor)

FOLDER_IMAGES = "images"


class MissionFolderError(Exception):
    pass


def check_mission_folder(mission_dir: str) -> None:
    """The folder must exist and contain an unbinarized mission.sqm."""
    folder = Path(mission_dir)
    if not folder.is_dir():
        raise MissionFolderError(f"{mission_dir} is not a folder.")
    sqm = folder / sqm_editor.MISSION_SQM
    if not sqm.is_file():
        raise MissionFolderError(
            "The selected folder does not contain a mission.sqm file.")
    head = sqm.read_bytes()[:16]
    if head.startswith(b"\0raP"):
        raise MissionFolderError(
            "mission.sqm is binarized. Save it unbinarized in Eden "
            "(or debinarize it) before running the loader.")


def generate_mission(config: MissionConfig) -> List[str]:
    """Generate every mission file; returns the paths written (for the UI)."""
    mission_dir = config.mission_dir
    check_mission_folder(mission_dir)
    written: List[Path] = []

    # 1. mission.sqm (backs up to mission.sqm.old)
    written.append(sqm_editor.edit_mission_sqm(mission_dir, config.mission))

    # 2. loadscreen image
    images = Path(mission_dir) / FOLDER_IMAGES
    images.mkdir(exist_ok=True)
    loadscreen = images / payload.LOADSCREEN
    shutil.copyfile(payload.loadscreen_path(), loadscreen)
    written.append(loadscreen)

    # 3. functions payload + common.hpp
    written += functions_payload.install_functions(
        mission_dir, config, payload.functions_root())

    # 4. scripts folder
    written.append(scripts_gen.write_infotext(mission_dir, config))
    for maybe in (
        scripts_gen.write_parameters_hpp(mission_dir, config.description),
        scripts_gen.write_briefing_loadout(mission_dir, config.description),
        scripts_gen.write_weather_script(mission_dir, config.weather),
    ):
        if maybe:
            written.append(maybe)

    # 5. briefing.sqf, debriefing.hpp
    written.append(briefing_gen.write_briefing(mission_dir, config))
    written.append(debriefing_gen.write_debriefing(mission_dir, config))

    # 6. description.ext, init.sqf
    written.append(description_ext.write_description_ext(mission_dir, config))
    written.append(init_sqf.write_init_sqf(mission_dir, config))

    return [str(p) for p in written]
