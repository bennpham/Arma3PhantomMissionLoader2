"""Edit an unbinarized mission.sqm in place (original mission.sqm.old backup).

Line-based port of the original loader's Form2_MissionSqmSettings: existing
attributes in ScenarioData / ScenarioData Header / Intel are replaced, missing
ones are filled in before each section closes, and CustomAttributes is fully
rewritten with the respawn button/template setup. Sections that do not exist
at all are appended.

WARNING (same as the original): any pre-existing CustomAttributes values are
replaced by the generated multiplayer respawn attributes.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterator, List, Optional

from ..model import MissionSettings

MISSION_SQM = "mission.sqm"
MISSION_SQM_BACKUP = "mission.sqm.old"


def _esc(text: str) -> str:
    return text.replace('"', '""')


def _one_line(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\n", " ")


def _multi_line(text: str) -> str:
    """Turn GUI newlines into the sqm string continuation `" \\n "`."""
    return text.replace("\r\n", "\n").replace("\n", '" \\n "')


def _pct(value: float) -> str:
    """0-100 UI value -> 0..1 sqm value, formatted like the original (0.3, 1, 0)."""
    return f"{value / 100:g}"


class _SqmEditor:
    def __init__(self, settings: MissionSettings):
        self.s = settings
        self.scenario_keys = {
            "author": False, "overviewText": False, "overViewPicture": False,
            "onLoadMission": False, "loadScreen": False, "aIKills": False,
            "respawn": False, "enableTeamSwitch": False, "class Header": False,
        }
        self.header_keys = {"gameType": False, "minPlayers": False, "maxPlayers": False}
        self.intel_keys = {
            "overviewText": False, "resistanceWest": False, "resistanceEast": False,
            "timeOfChanges": False, "startWeather": False, "startFog": False,
            "forecastWeather": False, "forecastFog": False,
            "year": False, "month": False, "day": False, "hour": False, "minute": False,
            "startFogBase": False, "forecastFogBase": False,
            "startFogDecay": False, "forecastFogDecay": False,
        }
        self.handled_scenario = False
        self.handled_custom_attributes = False
        self.handled_intel = False

    # ------------------------------------------------------------------ main
    def edit(self, lines: List[str]) -> List[str]:
        out: List[str] = []
        it = iter(lines)
        editing_scenario = editing_custom = editing_intel = False
        check_intel = False

        line = next(it, None)
        while line is not None:
            if editing_scenario or editing_custom or editing_intel:
                out.append(line)  # the section's opening "{"
                if editing_scenario:
                    self._handle_scenario_data(it, out)
                if editing_custom:
                    self._write_custom_attributes(it, out)
                if editing_intel:
                    self._handle_intel(it, out)
                editing_scenario = editing_custom = editing_intel = False
            else:
                # class Mission exists but carried no Intel: insert one right
                # before the closing brace of class Mission.
                if check_intel and not self.handled_intel and line == "};":
                    out.append("\tclass Intel")
                    out.append("\t{")
                    self._write_unused_intel(out)
                    out.append("\t};")
                    self.handled_intel = True
                out.append(line)

            if line == "class ScenarioData":
                editing_scenario = True
            elif line == "class CustomAttributes":
                editing_custom = True
            elif line == "\tclass Intel":
                editing_intel = True
            if line == "class Mission":
                check_intel = True
            line = next(it, None)

        # Sections missing from the file entirely get appended.
        if not self.handled_scenario:
            out.append("class ScenarioData")
            out.append("{")
            for cmd, used in list(self.scenario_keys.items()):
                if not used:
                    if cmd == "class Header":
                        out.append("\tclass Header")
                        out.append("\t{")
                        self._write_unused_header(out)
                        out.append("\t};")
                        self.scenario_keys[cmd] = True
                    else:
                        self._write_scenario_data(cmd, iter(()), out)
            out.append("};")
        if not self.handled_custom_attributes:
            out.append("class CustomAttributes")
            out.append("{")
            self._write_custom_attributes(iter(()), out)
        if not self.handled_intel:
            out.append("class Mission")
            out.append("{")
            out.append("\tclass Intel")
            out.append("\t{")
            self._write_unused_intel(out)
            out.append("\t};")
            out.append("};")
        return out

    # -------------------------------------------------------- ScenarioData
    def _handle_scenario_data(self, it: Iterator[str], out: List[str]) -> None:
        for line in it:
            self.handled_scenario = True
            handled = False
            key = line.strip().split("=")[0]
            for cmd in list(self.scenario_keys):
                if cmd == key:
                    handled = True
                    self._write_scenario_data(cmd, it, out, line)
            if line == "};":
                for cmd, used in list(self.scenario_keys.items()):
                    if not used:
                        self._write_scenario_data(cmd, it, out, line)
                out.append("};")
                return
            if not handled:
                out.append(line)

    def _write_scenario_data(self, cmd: str, it: Iterator[str], out: List[str],
                             line: Optional[str] = None) -> None:
        s = self.s
        if cmd == "author":
            out.append(f'\tauthor="{_esc(s.author)}";')
        elif cmd == "overviewText":
            out.append(f'\toverviewText="{_multi_line(_esc(s.overview_text))}";')
        elif cmd == "overViewPicture":
            out.append('\toverViewPicture="images\\loadscreen.jpg";')
        elif cmd == "onLoadMission":
            out.append(f'\tonLoadMission="{_one_line(_esc(s.on_load_mission))}";')
        elif cmd == "loadScreen":
            out.append('\tloadScreen="images\\loadscreen.jpg";')
        elif cmd == "aIKills":
            if s.allow_ai_score:
                out.append("\taIKills=1;")
        elif cmd == "respawn":
            out.append("\trespawn=5;")
        elif cmd == "enableTeamSwitch":
            if not s.enable_team_switch:
                out.append("\tenableTeamSwitch=0;")
        elif cmd == "class Header":
            out.append("\tclass Header")
            self._handle_header(it, out, line)
        self.scenario_keys[cmd] = True

    def _handle_header(self, it: Iterator[str], out: List[str],
                       line: Optional[str]) -> None:
        if line is None or line == "\tclass Header":
            line = next(it, None)
        while line is not None:
            if line == "};":
                out.append("\t{")
            handled = False
            key = line.strip().split("=")[0]
            for cmd in list(self.header_keys):
                if cmd == key:
                    handled = True
                    self._write_header(cmd, out)
            if line in ("\t};", "};"):
                self._write_unused_header(out)
                out.append("\t};")
                return
            if not handled:
                out.append(line)
            line = next(it, None)

    def _write_unused_header(self, out: List[str]) -> None:
        for cmd, used in list(self.header_keys.items()):
            if not used:
                self._write_header(cmd, out)

    def _write_header(self, cmd: str, out: List[str]) -> None:
        s = self.s
        if cmd == "gameType":
            out.append('\t\tgameType="Coop";')
        elif cmd == "minPlayers":
            out.append(f"\t\tminPlayers={s.min_players};")
        elif cmd == "maxPlayers":
            out.append(f"\t\tmaxPlayers={s.max_players};")
        self.header_keys[cmd] = True

    # ---------------------------------------------------- CustomAttributes
    def _write_custom_attributes(self, it: Iterator[str], out: List[str]) -> None:
        s = self.s
        self.handled_custom_attributes = True
        out.append("\tclass Category0")
        out.append("\t{")
        out.append('\t\tname="Multiplayer";')
        out.append("\t\tclass Attribute0")
        out.append("\t\t{")
        out.append('\t\t\tproperty="RespawnButton";')
        out.append('\t\t\texpression="true";')
        out.append("\t\t\tclass Value")
        out.append("\t\t\t{")
        out.append("\t\t\t\tclass data")
        out.append("\t\t\t\t{")
        out.append("\t\t\t\t\tclass type")
        out.append("\t\t\t\t\t{")
        out.append("\t\t\t\t\t\ttype[]=")
        out.append("\t\t\t\t\t\t{")
        out.append('\t\t\t\t\t\t\t"SCALAR"')
        out.append("\t\t\t\t\t\t};")
        out.append("\t\t\t\t\t};")
        out.append(f"\t\t\t\t\tvalue={1 if s.manual_respawn else 0};")
        out.append("\t\t\t\t};")
        out.append("\t\t\t};")
        out.append("\t\t};")
        out.append("\t\tclass Attribute1")
        out.append("\t\t{")
        out.append('\t\t\tproperty="RespawnTemplates";')
        out.append('\t\t\texpression="true";')
        out.append("\t\t\tclass Value")
        out.append("\t\t\t{")
        out.append("\t\t\t\tclass data")
        out.append("\t\t\t\t{")
        out.append("\t\t\t\t\tclass type")
        out.append("\t\t\t\t\t{")
        out.append("\t\t\t\t\t\ttype[]=")
        out.append("\t\t\t\t\t\t{")
        out.append('\t\t\t\t\t\t\t"ARRAY"')
        out.append("\t\t\t\t\t\t};")
        out.append("\t\t\t\t\t};")
        self._write_respawn_templates(out)
        out.append("\t\t\t\t};")
        out.append("\t\t\t};")
        out.append("\t\t};")
        out.append("\t\tnAttributes=2;")
        out.append("\t};")
        out.append("};")
        # Skip the original CustomAttributes content up to its closing brace.
        for line in it:
            if line == "};":
                return

    def _write_respawn_templates(self, out: List[str]) -> None:
        s = self.s
        rule_sets = []
        if s.mp_mission_fail:
            rule_sets.append("EndMission")
        if s.mp_sp_death_screen:
            rule_sets.append("None")
        if s.mp_switch_char:
            rule_sets.append("SwitchPlayer")
        if not rule_sets:
            return
        out.append("\t\t\t\t\tclass value")
        out.append("\t\t\t\t\t{")
        out.append(f"\t\t\t\t\t\titems={len(rule_sets)};")
        for i, rule in enumerate(rule_sets):
            out.append(f"\t\t\t\t\t\tclass Item{i}")
            out.append("\t\t\t\t\t\t{")
            out.append("\t\t\t\t\t\t\tclass data")
            out.append("\t\t\t\t\t\t\t{")
            out.append("\t\t\t\t\t\t\t\tclass type")
            out.append("\t\t\t\t\t\t\t\t{")
            out.append("\t\t\t\t\t\t\t\t\ttype[]=")
            out.append("\t\t\t\t\t\t\t\t\t{")
            out.append('\t\t\t\t\t\t\t\t\t\t"STRING"')
            out.append("\t\t\t\t\t\t\t\t\t};")
            out.append("\t\t\t\t\t\t\t\t};")
            out.append(f'\t\t\t\t\t\t\t\tvalue="{rule}";')
            out.append("\t\t\t\t\t\t\t};")
            out.append("\t\t\t\t\t\t};")
        out.append("\t\t\t\t\t};")

    # ------------------------------------------------------------- Intel
    def _handle_intel(self, it: Iterator[str], out: List[str]) -> None:
        for line in it:
            self.handled_intel = True
            handled = False
            key = line.strip().split("=")[0]
            for cmd in list(self.intel_keys):
                if cmd == key:
                    handled = True
                    self._write_intel(cmd, out)
            if line == "\t};":
                self._write_unused_intel(out)
                out.append("\t};")
                return
            if not handled:
                out.append(line)

    def _write_unused_intel(self, out: List[str]) -> None:
        for cmd, used in list(self.intel_keys.items()):
            if not used:
                self._write_intel(cmd, out)

    def _write_intel(self, cmd: str, out: List[str]) -> None:
        s = self.s
        if cmd == "overviewText":
            out.append(f'\t\toverviewText="{_one_line(_esc(s.summary))}";')
        elif cmd == "resistanceWest":
            out.append(f"\t\tresistanceWest={1 if s.resistance_west else 0};")
        elif cmd == "resistanceEast":
            out.append(f"\t\tresistanceEast={1 if s.resistance_east else 0};")
        elif cmd == "timeOfChanges":
            toc = min(s.toc_hours * 3600 + s.toc_minutes * 60 + s.toc_seconds, 28800)
            out.append(f"\t\ttimeOfChanges={toc};")
        elif cmd == "startWeather":
            out.append(f"\t\tstartWeather={_pct(s.overcast_start)};")
        elif cmd == "startFog":
            out.append(f"\t\tstartFog={_pct(s.fog_start)};")
        elif cmd == "forecastWeather":
            out.append(f"\t\tforecastWeather={_pct(s.overcast_forecast)};")
        elif cmd == "forecastFog":
            out.append(f"\t\tforecastFog={_pct(s.fog_forecast)};")
        elif cmd == "startFogBase":
            out.append(f"\t\tstartFogBase={s.fog_start_base};")
        elif cmd == "forecastFogBase":
            out.append(f"\t\tforecastFogBase={s.fog_forecast_base};")
        elif cmd == "startFogDecay":
            out.append(f"\t\tstartFogDecay={_pct(s.fog_start_decay)};")
        elif cmd == "forecastFogDecay":
            out.append(f"\t\tforecastFogDecay={_pct(s.fog_forecast_decay)};")
        elif cmd == "year":
            out.append(f"\t\tyear={s.year};")
        elif cmd == "month":
            out.append(f"\t\tmonth={s.month};")
        elif cmd == "day":
            out.append(f"\t\tday={s.day};")
        elif cmd == "hour":
            out.append(f"\t\thour={s.hour};")
        elif cmd == "minute":
            out.append(f"\t\tminute={s.minute};")
        self.intel_keys[cmd] = True


def edit_mission_sqm(mission_dir: str, settings: MissionSettings) -> Path:
    """Back up mission.sqm to mission.sqm.old and write the edited version."""
    mission_sqm = Path(mission_dir) / MISSION_SQM
    backup = Path(mission_dir) / MISSION_SQM_BACKUP
    if backup.exists():
        backup.unlink()
    mission_sqm.rename(backup)

    text = backup.read_text(encoding="utf-8", errors="surrogateescape")
    lines = text.replace("\r\n", "\n").split("\n")
    edited = _SqmEditor(settings).edit(lines)
    mission_sqm.write_text("\n".join(edited) + "\n",
                           encoding="utf-8", errors="surrogateescape")
    return mission_sqm
