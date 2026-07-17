"""Generate scripts/briefing.sqf: FHQ TaskTracker briefing + task arrays."""
from __future__ import annotations

from pathlib import Path
from typing import List

from ..model import BriefingEntry, MissionConfig, TaskEntry

FOLDER_SCRIPTS = "scripts"
BRIEFING = "briefing.sqf"

HEADER = '''_color = ["GUI", "BCG_RGB"] call BIS_fnc_displayColorGet;
_htmlcolor = _color call BIS_fnc_colorRGBAtoHTML;

#define __color_link(marker, text) "<font color='" + _htmlcolor + "'><marker name='" + marker + "'>" + text + "</marker></font>"
#define __color_text(text) "<font color='" + _htmlcolor + "'>" + text + "</font>"
#define __color_clink(colour, marker, text) "<font color='" + colour + "'><marker name='" + marker + "'>" + text + "</marker></font>"
#define __color_ctext(colour, text) "<font color='" + colour + "'>" + text + "</font>"

/* Briefing
 * The briefing can be defined by calling FHQ_TT_addBriefing.
 * The array is built like this.
 * The first element should be a filter (side, group, faction, or a piece of script)
 * This is followed by pairs of strings, a head line, and an actual text.
 * Briefings are added in the order in which they appear for any unit that matches
 * the last filter.
 */
'''


def _esc_description(text: str) -> str:
    """Escape quotes and newlines for an SQF string, keeping the _htmlcolor
    concatenation produced by the Color/Marker helper buttons intact."""
    escaped = text.replace('"', '""').replace("\r\n", "\n").replace("\n", "<br/>")
    return escaped.replace("'\"\" + _htmlcolor + \"\"'", "'\" + _htmlcolor + \"'")


def _esc(text: str) -> str:
    return text.replace('"', '""')


def _briefing_block(entries: List[BriefingEntry]) -> str:
    items = []
    for entry in entries:
        items.append('\t\t["%s",\n\t\t\t"%s"]'
                     % (_esc(entry.title), _esc_description(entry.description)))
    return "[\n\t{true}, \n" + ",\n\n".join(items) + "\n\n\n] call FHQ_fnc_ttAddBriefing;\n"


def _task_block(tasks: List[TaskEntry]) -> str:
    items = []
    for task in tasks:
        items.append(
            '    \t["%s", // Task name\n'
            '\t\t "%s", // Task Description\n'
            '\t\t "%s", // Task title in briefing\n'
            '\t\t "%s", // Waypoint text\n'
            '\t\t getmarkerpos "%s", // Optional: Position or object\n'
            '\t\t "%s", // Optional: Task State Status\n'
            '\t\t "%s" // Optional: Task Type\n'
            "        ]"
            % (task.name, _esc_description(task.description), _esc(task.title),
               _esc(task.waypoint_text), task.marker, task.state, task.task_type))
    return "\n[\n\t{true},\n" + ",\n".join(items) + "\n] call FHQ_fnc_ttAddTasks;\n"


def write_briefing(mission_dir: str, config: MissionConfig) -> Path:
    parts = [HEADER]
    if config.briefings:
        parts.append(_briefing_block(config.briefings))
    if config.tasks:
        parts.append(_task_block(config.tasks))
    path = Path(mission_dir) / FOLDER_SCRIPTS / BRIEFING
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts), encoding="utf-8")
    return path
