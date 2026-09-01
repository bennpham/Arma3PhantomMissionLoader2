"""Server-side setup blocks shared by init.sqf and functions\\pht6\\main.sqf.

Depending on the "Use main.sqf" option these blocks are emitted either inline in
init.sqf or, indented one level, inside the PHT6_fnc_main body.
"""
from __future__ import annotations

from typing import List


def ace_block() -> List[str]:
    return [
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


def scale_players_block() -> List[str]:
    return [
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


def zeus_block() -> List[str]:
    return [
        "// Initialize stuff for Zeus on server",
        "if (isMultiplayer && isServer) then {",
        "\t{zeus_mod1 addCuratorEditableObjects [[_x],true]} forEach allUnits;",
        "\t{zeus_mod2 addCuratorEditableObjects [[_x],true]} forEach allUnits;",
        "\t{zeus_mod3 addCuratorEditableObjects [[_x],true]} forEach allUnits;",
        "};",
    ]


def indent(lines: List[str], prefix: str = "\t") -> List[str]:
    """Indent every non-empty line, leaving blank lines free of trailing space."""
    return [prefix + line if line else line for line in lines]
