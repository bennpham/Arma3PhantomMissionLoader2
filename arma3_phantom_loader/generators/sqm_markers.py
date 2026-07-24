"""Read marker names out of an unbinarized mission.sqm.

Markers live as `class ItemN` blocks under `class Mission > class Entities`,
distinguished from units/groups/triggers by `dataType="Marker"`. Their
scripting handle is the `name` attribute (e.g. `name="start"`), which is what
SQF addresses via `getMarkerPos`. This is separate from `type=` (the icon).

Parsing mirrors the line-based style of sqm_editor: the file is read leniently
(surrogateescape) and never raises for the UI's sake — a missing, binarized or
unreadable mission.sqm just yields no markers.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

MISSION_SQM = "mission.sqm"

_NAME_RE = re.compile(r'name\s*=\s*"(.*?)"\s*;')


def parse_marker_names(mission_dir: str) -> List[str]:
    """Return sorted, unique names of `dataType="Marker"` entries.

    Missing / binarized / unreadable mission.sqm returns [] (never raises).
    """
    sqm = Path(mission_dir) / MISSION_SQM
    try:
        raw = sqm.read_bytes()
    except OSError:
        return []
    if raw[:4] == b"\0raP":  # binarized: nothing to parse
        return []

    text = raw.decode("utf-8", errors="surrogateescape")
    lines = text.replace("\r\n", "\n").split("\n")

    names: set[str] = set()
    depth = 0
    marker_depth: int | None = None  # depth of the current marker's block

    for line in lines:
        stripped = line.strip()

        # Close before descending would misattribute names, so handle braces
        # around the content on their own lines (sqm is one token per line).
        if stripped in ("};", "}"):
            depth -= 1
            if marker_depth is not None and depth < marker_depth:
                marker_depth = None
            continue
        if stripped == "{":
            depth += 1
            continue

        if stripped == 'dataType="Marker";':
            marker_depth = depth
            continue

        if marker_depth is not None and depth == marker_depth:
            match = _NAME_RE.match(stripped)
            if match:
                name = match.group(1)
                if name:
                    names.add(name)
                marker_depth = None  # captured this marker's name

    return sorted(names)
