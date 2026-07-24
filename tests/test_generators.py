"""Generator tests: run the pipeline against the fixture mission folder."""
import shutil
from pathlib import Path

import pytest

from arma3_phantom_loader import payload
from arma3_phantom_loader.generators.sqm_markers import parse_marker_names
from arma3_phantom_loader.model import (BriefingEntry, DebriefEntry,
                                        MissionConfig, TaskEntry,
                                        ordered_tasks)
from arma3_phantom_loader.pipeline import (MissionFolderError,
                                           check_mission_folder,
                                           generate_mission)

FIXTURE = Path(__file__).parent / "fixtures" / "mission_folder"


@pytest.fixture
def mission_dir(tmp_path):
    target = tmp_path / "test_mission.Altis"
    shutil.copytree(FIXTURE, target)
    return target


def base_config(mission_dir) -> MissionConfig:
    config = MissionConfig(mission_dir=str(mission_dir))
    config.mission.author = "Benn"
    config.mission.on_load_name = "Operation Test"
    config.mission.on_load_mission = 'A "test" mission'
    config.mission.overview_text = "Line one\nLine two"
    config.mission.summary = "Attack the town.\nThen hold it."
    config.mission.min_players = 2
    config.mission.max_players = 12
    config.mission.overcast_start = 30
    config.mission.toc_hours = 9  # deliberately over the 28800s cap
    config.debriefings = [
        DebriefEntry(classname="Win", title="Mission Accomplished",
                     subtitle="Well done", description='You "won" it'),
        DebriefEntry(classname="Lose", title="Mission Failed"),
    ]
    config.briefings = [
        BriefingEntry(title="Situation", description="Enemy ahead\nBe careful"),
    ]
    config.tasks = [
        TaskEntry(name="task1", title="Clear town", description="Clear it",
                  waypoint_text="Clear", marker="mkr1", state="assigned"),
        TaskEntry(name="task1a", parent="task1", title="Curly",
                  description="Eliminate the intelligence officer",
                  waypoint_text="officers", marker="mkr1", task_type="kill"),
    ]
    return config


# --------------------------------------------------------------- validation
def test_validate_catches_problems():
    config = MissionConfig()
    config.tasks = [TaskEntry(name="t1", title="A", state="assigned"),
                    TaskEntry(name="t1", title="B", state="assigned")]
    problems = config.validate()
    assert any("mission folder" in p.lower() for p in problems)
    assert any("debriefing" in p.lower() for p in problems)
    assert any("Duplicate task name" in p for p in problems)
    assert any("assigned" in p for p in problems)


def test_validate_catches_parent_problems():
    config = MissionConfig()
    config.tasks = [TaskEntry(name="t1", title="A", parent="nope"),
                    TaskEntry(name="t2", title="B", parent="t2"),
                    TaskEntry(name="t3", title="C", parent="t4"),
                    TaskEntry(name="t4", title="D", parent="t3")]
    problems = config.validate()
    assert any("unknown parent task 'nope'" in p for p in problems)
    assert any("Task 't2' cannot be its own parent." == p for p in problems)
    assert any("Task 't3' is part of a parent/child loop." == p for p in problems)
    assert any("Task 't4' is part of a parent/child loop." == p for p in problems)


def test_validate_accepts_nested_subtasks():
    config = MissionConfig(mission_dir="somewhere")
    config.debriefings = [DebriefEntry(classname="Win", title="Won")]
    config.tasks = [TaskEntry(name="t1", title="A"),
                    TaskEntry(name="t1a", title="B", parent="t1"),
                    TaskEntry(name="t1a1", title="C", parent="t1a")]
    assert config.validate() == []


# ------------------------------------------------------------ task ordering
def test_ordered_tasks_puts_parents_first():
    child = TaskEntry(name="t1a", parent="t1")
    grandchild = TaskEntry(name="t1a1", parent="t1a")
    parent = TaskEntry(name="t1")
    other = TaskEntry(name="t2")
    ordered = ordered_tasks([child, grandchild, parent, other])
    assert [(task.name, depth) for task, depth in ordered] == [
        ("t1", 0), ("t1a", 1), ("t1a1", 2), ("t2", 0)]


def test_ordered_tasks_keeps_every_task_in_a_loop():
    looped = [TaskEntry(name="t1", parent="t2"), TaskEntry(name="t2", parent="t1")]
    ordered = ordered_tasks(looped)
    assert sorted(task.name for task, _ in ordered) == ["t1", "t2"]


def test_check_mission_folder_rejects_binarized(tmp_path):
    (tmp_path / "mission.sqm").write_bytes(b"\0raP\0\0\0\0garbage")
    with pytest.raises(MissionFolderError, match="binarized"):
        check_mission_folder(str(tmp_path))


def test_check_mission_folder_rejects_missing(tmp_path):
    with pytest.raises(MissionFolderError, match="mission.sqm"):
        check_mission_folder(str(tmp_path))


# -------------------------------------------------------------- mission.sqm
def test_sqm_edit(mission_dir):
    config = base_config(mission_dir)
    generate_mission(config)

    assert (mission_dir / "mission.sqm.old").is_file()
    text = (mission_dir / "mission.sqm").read_text()

    # ScenarioData replaced/filled
    assert 'author="Benn";' in text
    assert "respawn=5;" in text
    assert 'loadScreen="images\\loadscreen.jpg";' in text
    assert 'overviewText="Line one" \\n "Line two";' in text
    assert 'onLoadMission="A ""test"" mission";' in text
    # Header: gameType replaced, minPlayers added, maxPlayers replaced
    assert 'gameType="Coop";' in text
    assert "minPlayers=2;" in text
    assert "maxPlayers=12;" in text
    assert 'gameType="ZvZ";' not in text

    # CustomAttributes fully rewritten
    assert "SomethingOld" not in text
    assert 'property="RespawnButton";' in text
    assert 'property="RespawnTemplates";' in text
    assert 'value="EndMission";' in text
    assert 'value="None";' in text
    assert 'value="SwitchPlayer";' not in text  # unchecked by default

    # Intel replaced/filled, cap applied
    assert "timeOfChanges=28800;" in text
    assert "startWeather=0.3;" in text
    assert "resistanceWest=1;" in text
    assert 'overviewText="Attack the town. Then hold it.";' in text
    # untouched line kept as-is
    assert "startWind=0.1;" in text
    # entities preserved
    assert 'dataType="Group";' in text

    # loadscreen copied
    assert (mission_dir / "images" / "loadscreen.jpg").is_file()


# ---------------------------------------------------------------- functions
def test_functions_mandatory_only(mission_dir):
    config = base_config(mission_dir)
    generate_mission(config)

    functions = mission_dir / "functions"
    for name in ["fhq_ai", "fhq_misc", "fhq_tasktracker"]:
        assert (functions / name).is_dir()
        assert (functions / f"{name}.hpp").is_file()
    assert not (functions / "taw_vd").exists()
    assert not (functions / "weatherEffects.fsm").exists()

    common = (functions / "common.hpp").read_text()
    assert '#include "fhq_ai.hpp"' in common
    assert '#include "fhq_misc.hpp"' in common
    assert '#include "fhq_tasktracker.hpp"' in common
    assert "taw_vd" not in common
    assert "class FHQ" in common
    assert "#define EXPORTED_FUNCTION" in common


def test_functions_with_taw_and_weather(mission_dir):
    config = base_config(mission_dir)
    config.taw_vd.enabled = True
    config.taw_vd.disable_none = True
    config.taw_vd.enable_max_range = True
    config.taw_vd.max_range = 12000
    config.weather.enabled = True
    config.weather.fog = True
    config.weather.fog_interval = 5
    config.weather.snow = True
    config.weather.snow_interval = 7
    generate_mission(config)

    functions = mission_dir / "functions"
    assert (functions / "taw_vd" / "CfgFunctions.hpp").is_file()
    assert (functions / "weatherEffects.fsm").is_file()
    assert '#include "taw_vd\\CfgFunctions.hpp"' in (functions / "common.hpp").read_text()

    weather = (mission_dir / "scripts" / "weatherScript.sqf").read_text()
    assert '["fog", {true}]' in weather
    assert '["snow", {true}]' in weather
    assert '["sand", {true}]' not in weather
    assert '[_handle, "fogInterval", 5] call FHQ_fnc_setWeatherEffect;' in weather
    assert '[_handle, "snowInterval", 7] call FHQ_fnc_setWeatherEffect;' in weather
    assert "FHQ_fnc_weatherEffect" in weather

    init = (mission_dir / "init.sqf").read_text()
    assert 'call compile preProcessFileLineNumbers "scripts\\weatherScript.sqf";' in init
    assert "tawvd_disablenone = true;" in init
    assert "tawvd_maxRange = 12000;" in init

    description = (mission_dir / "description.ext").read_text()
    assert '#include "functions\\taw_vd\\GUI.h"' in description


# ---------------------------------------------------- description.ext / init
def test_description_and_init_defaults(mission_dir):
    config = base_config(mission_dir)
    generate_mission(config)

    description = (mission_dir / "description.ext").read_text()
    assert 'author="Benn";' in description
    assert 'OnLoadName = "Operation Test";' in description
    assert "minPlayers = 2;" in description
    assert "maxPlayers = 12;" in description
    assert '#include "debriefing.hpp"' in description
    assert '#include "functions\\common.hpp"' in description
    assert "class Params" not in description
    assert "briefing_loadout" not in description
    assert "taw_vd" not in description

    init = (mission_dir / "init.sqf").read_text()
    assert 'call compile preProcessFileLineNumbers "scripts\\briefing.sqf";' in init
    assert 'call compile preProcessFileLineNumbers "scripts\\infotext.sqf";' in init
    assert "weatherScript" not in init
    assert "CfgMods" not in init
    assert "zeus_mod1" not in init


def test_description_and_init_all_options(mission_dir):
    config = base_config(mission_dir)
    config.description.params_scale_players = True
    config.description.params_fhq_difficulty = True
    config.description.description_loadout = True
    config.description.init_ace = True
    config.description.init_zeus = True
    generate_mission(config)

    description = (mission_dir / "description.ext").read_text()
    assert '#include "scripts\\parameters.hpp"' in description
    assert '#include "scripts\\briefing_loadout.hpp"' in description

    parameters = (mission_dir / "scripts" / "parameters.hpp").read_text()
    assert "class ScalePlayers" in parameters
    assert "class FHQ_Difficulty" in parameters
    assert (mission_dir / "scripts" / "briefing_loadout.hpp").is_file()

    init = (mission_dir / "init.sqf").read_text()
    assert '"ScalePlayers" call BIS_fnc_getParamValue' in init
    assert 'isClass (configFile >> "CfgMods" >> "ace")' in init
    assert "zeus_mod1 addCuratorEditableObjects" in init


# -------------------------------------------------------- briefing/debriefing
def test_briefing_and_tasks(mission_dir):
    config = base_config(mission_dir)
    generate_mission(config)

    briefing = (mission_dir / "scripts" / "briefing.sqf").read_text()
    assert "BIS_fnc_displayColorGet" in briefing
    assert '["Situation",' in briefing
    assert "Enemy ahead<br/>Be careful" in briefing
    assert "] call FHQ_fnc_ttAddBriefing;" in briefing
    assert '["task1", // Task name' in briefing
    assert 'getmarkerpos "mkr1"' in briefing
    assert '"assigned", // Optional: Task State Status' in briefing
    assert "] call FHQ_fnc_ttAddTasks;" in briefing


def test_subtasks_use_the_array_form_after_their_parent(mission_dir):
    config = base_config(mission_dir)
    # Deliberately listed child first: the generator must still write the parent
    # first, or FHQ_fnc_ttiCreateOrUpdateTask gets a nil parent.
    config.tasks = [
        TaskEntry(name="task1a1", parent="task1a", title="Deeper"),
        TaskEntry(name="task1a", parent="task1", title="Curly"),
        TaskEntry(name="task1", title="Kill the officers"),
    ]
    generate_mission(config)

    briefing = (mission_dir / "scripts" / "briefing.sqf").read_text()
    assert '["task1", // Task name' in briefing
    assert '[["task1a", "task1"], // Task name' in briefing
    assert '[["task1a1", "task1a"], // Task name' in briefing
    assert (briefing.index('["task1", //')
            < briefing.index('[["task1a", "task1"]')
            < briefing.index('[["task1a1", "task1a"]'))


def test_debriefing(mission_dir):
    config = base_config(mission_dir)
    generate_mission(config)

    debriefing = (mission_dir / "debriefing.hpp").read_text()
    assert "class Win" in debriefing
    assert 'title = "Mission Accomplished";' in debriefing
    assert 'description = "You ""won"" it";' in debriefing
    assert "class Lose" in debriefing


def test_infotext(mission_dir):
    config = base_config(mission_dir)
    config.description.infotext = "Operation Test\nBy the community"
    generate_mission(config)

    infotext = (mission_dir / "scripts" / "infotext.sqf").read_text()
    assert '["June 24, 2035", "12:00:00"] call BIS_fnc_infoText;' in infotext
    assert '["Operation Test", "By the community"] call BIS_fnc_infoText;' in infotext
    assert '["Created by","Benn"] call BIS_fnc_infoText;' in infotext


# ------------------------------------------------------------- marker parser
def test_parse_marker_names_from_fixture(mission_dir):
    # The fixture has two markers plus a named non-marker object in a group.
    assert parse_marker_names(str(mission_dir)) == ["objective", "start"]


def test_parse_marker_names_missing_file(tmp_path):
    assert parse_marker_names(str(tmp_path)) == []


def test_parse_marker_names_binarized(tmp_path):
    (tmp_path / "mission.sqm").write_bytes(b"\0raP\0\0\0\0garbage")
    assert parse_marker_names(str(tmp_path)) == []


def test_parse_marker_names_ignores_unnamed_and_dedupes(tmp_path):
    (tmp_path / "mission.sqm").write_text(
        "class Mission\n{\nclass Entities\n{\n"
        'class Item0\n{\ndataType="Marker";\nname="a";\n};\n'
        'class Item1\n{\ndataType="Marker";\ntype="mil_dot";\n};\n'  # no name
        'class Item2\n{\ndataType="Marker";\nname="a";\n};\n'  # dup
        "};\n};\n")
    assert parse_marker_names(str(tmp_path)) == ["a"]


# ------------------------------------------------------------------ payload
def test_embedded_payload_resolves():
    root = payload.functions_root()
    assert (root / "fhq_ai.hpp").is_file()
    assert (root / "weatherEffects.fsm").is_file()
    assert payload.loadscreen_path().is_file()


def test_payload_env_override(tmp_path, monkeypatch):
    override = tmp_path / "custom"
    (override / "functions").mkdir(parents=True)
    monkeypatch.setenv("ARMA3PML_PAYLOAD", str(override))
    assert payload.payload_root() == override
    # loadscreen falls back to the embedded copy
    assert payload.loadscreen_path().is_file()


# ----------------------------------------------------------------- reruns
def test_regenerate_is_idempotent(mission_dir):
    config = base_config(mission_dir)
    generate_mission(config)
    generate_mission(config)  # must not raise on existing files/backup

    text = (mission_dir / "mission.sqm").read_text()
    # the second run edits the first run's output; keys must not duplicate
    assert text.count("respawn=5;") == 1
    assert text.count('gameType="Coop";') == 1
