"""Generate init.sqf."""
from __future__ import annotations

from pathlib import Path
from typing import List

from ..model import MissionConfig

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

    if config.taw_vd.enabled:
        lines.append("")
        lines.append("// TAW View Distance settings")
        if config.taw_vd.disable_none:
            lines.append("tawvd_disablenone = true;")
        if config.taw_vd.enable_max_range:
            lines.append(f"tawvd_maxRange = {config.taw_vd.max_range};")

    if desc.init_ace:
        lines += [
            "",
            "// Adds extra ace equipments to player's uniforms or vests.",
            '//\tExample 1: ammobox1 addItemCargoGlobal ["ACE_bloodIV", 2];',
            '//\tExample 2: uniformContainer p1 addMagazineCargoGlobal ["ACE_M84", 6];',
            'if (isServer && isClass (configFile >> "CfgMods" >> "ace")) then {',
            "\t{",
            '\t\tvestContainer _x addItemCargoGlobal ["ACE_EarPlugs", 1];',
            "",
            "\t\t// Give medics medical supplies",
            '\t\tif (_x getUnitTrait "medic" == true) then {',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_bloodIV", 3];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_salineIV", 3];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_bloodIV_500", 2];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_salineIV_500", 2];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_bloodIV_250", 3];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_salineIV_250", 3];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_epinephrine", 6];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_morphine", 8];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_tourniquet", 4];',
            '\t\t\tbackpackContainer _x addItemCargoGlobal ["ACE_splint", 6];',
            "\t\t};",
            "",
            "\t\t// TODO",
            "\t} forEach FHQ_playableUnits;",
            "};",
        ]
    if desc.params_scale_players:
        lines += [
            "",
            "// Singleplayer handling",
            "if (!isMultiplayer) then {",
            "\t// TODO",
            "};",
            "",
            "// Scaled Multiplayer handling for small player count",
            '_ScalePlayers = "ScalePlayers" call BIS_fnc_getParamValue;',
            "if (_ScalePlayers == 1 && isServer && isMultiplayer) then {",
            "\t// TODO",
            "};",
            "",
            "// Fullhouse Multiplayer Handling",
            "if (_ScalePlayers == 0 && isServer && isMultiplayer) then {",
            "\t// TODO",
            "};",
        ]
    if desc.init_zeus:
        lines += [
            "",
            "// Initialize stuff for Zeus on server",
            "if (isMultiplayer && isServer) then {",
            "\t{zeus_mod1 addCuratorEditableObjects [[_x],true]} forEach allUnits;",
            "\t{zeus_mod2 addCuratorEditableObjects [[_x],true]} forEach allUnits;",
            "\t{zeus_mod3 addCuratorEditableObjects [[_x],true]} forEach allUnits;",
            "};",
        ]
    lines.append("")
    if config.weather.enabled:
        lines.append('call compile preProcessFileLineNumbers "scripts\\weatherScript.sqf";')
    lines.append('call compile preProcessFileLineNumbers "scripts\\infotext.sqf";')

    path = Path(mission_dir) / INIT
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
