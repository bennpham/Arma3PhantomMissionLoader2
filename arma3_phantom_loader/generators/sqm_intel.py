"""Read the `class Intel` block out of an unbinarized mission.sqm.

`class Intel` lives under `class Mission` and carries the mission's date/time,
the resistance (Independent-side friendliness) flags, and the weather/fog
settings — the same set of fields sqm_editor writes. This reader is the inverse
of that writer, so the Mission tab can reflect a loaded mission instead of its
hard-coded defaults.

Parsing mirrors the lenient, line-based style of sqm_markers: the file is read
leniently (surrogateescape) and never raises for the UI's sake — a missing,
binarized or unreadable mission.sqm just yields an empty `IntelValues()`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

MISSION_SQM = "mission.sqm"


@dataclass
class IntelValues:
    """Raw values read straight from `class Intel` (sqm scale, unconverted).

    Every field is Optional: `None` means the key was absent from the file, so
    callers leave the corresponding widget untouched.
    """
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    resistance_west: Optional[bool] = None
    resistance_east: Optional[bool] = None
    time_of_changes: Optional[float] = None   # seconds
    start_weather: Optional[float] = None      # 0..1 (sqm scale)
    forecast_weather: Optional[float] = None   # 0..1
    start_fog: Optional[float] = None          # 0..1
    forecast_fog: Optional[float] = None       # 0..1
    start_fog_base: Optional[float] = None     # metres, raw
    forecast_fog_base: Optional[float] = None  # metres, raw
    start_fog_decay: Optional[float] = None    # 0..1
    forecast_fog_decay: Optional[float] = None  # 0..1


# sqm key -> (IntelValues attribute, converter). Keys the tool has no widget for
# (startWind, startWaves, forecast{Wind,Waves,Lightnings}) are deliberately
# omitted so they pass through untouched on the next save.
_INT = int
_FLOAT = float
_BOOL = lambda v: bool(int(float(v)))

_FIELDS: dict[str, tuple[str, object]] = {
    "year": ("year", _INT),
    "month": ("month", _INT),
    "day": ("day", _INT),
    "hour": ("hour", _INT),
    "minute": ("minute", _INT),
    "resistanceWest": ("resistance_west", _BOOL),
    "resistanceEast": ("resistance_east", _BOOL),
    "timeOfChanges": ("time_of_changes", _FLOAT),
    "startWeather": ("start_weather", _FLOAT),
    "forecastWeather": ("forecast_weather", _FLOAT),
    "startFog": ("start_fog", _FLOAT),
    "forecastFog": ("forecast_fog", _FLOAT),
    "startFogBase": ("start_fog_base", _FLOAT),
    "forecastFogBase": ("forecast_fog_base", _FLOAT),
    "startFogDecay": ("start_fog_decay", _FLOAT),
    "forecastFogDecay": ("forecast_fog_decay", _FLOAT),
}

_ASSIGN_RE = re.compile(r'^([A-Za-z]+)\s*=\s*(-?\d+(?:\.\d+)?)\s*;$')


def parse_intel(mission_dir: str) -> IntelValues:
    """Return the values found in `class Intel` (fields absent stay None).

    Missing / binarized / unreadable mission.sqm returns an empty
    `IntelValues()` (never raises).
    """
    values = IntelValues()

    sqm = Path(mission_dir) / MISSION_SQM
    try:
        raw = sqm.read_bytes()
    except OSError:
        return values
    if raw[:4] == b"\0raP":  # binarized: nothing to parse
        return values

    text = raw.decode("utf-8", errors="surrogateescape")
    lines = text.replace("\r\n", "\n").split("\n")

    depth = 0
    intel_depth: int | None = None  # brace depth just inside `class Intel`

    for line in lines:
        stripped = line.strip()

        # sqm writes one token per line; handle the braces on their own lines.
        if stripped in ("};", "}"):
            depth -= 1
            if intel_depth is not None and depth < intel_depth:
                intel_depth = None  # left the Intel block
            continue
        if stripped == "{":
            depth += 1
            continue

        if stripped == "class Intel":
            # The block's "{" comes on the next line; record the depth its
            # contents will sit at.
            intel_depth = depth + 1
            continue

        # Only read assignments that sit directly inside `class Intel`.
        if intel_depth is None or depth != intel_depth:
            continue

        match = _ASSIGN_RE.match(stripped)
        if not match:
            continue
        key, rawval = match.group(1), match.group(2)
        field = _FIELDS.get(key)
        if field is None:
            continue
        attr, convert = field
        setattr(values, attr, convert(rawval))

    return values
