"""Generate debriefing.hpp (included by CfgDebriefing in description.ext)."""
from __future__ import annotations

from pathlib import Path

from ..model import MissionConfig

DEBRIEFING = "debriefing.hpp"


def _esc(text: str) -> str:
    return text.replace('"', '""')


def _one_line(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\n", " ")


def write_debriefing(mission_dir: str, config: MissionConfig) -> Path:
    lines = []
    for entry in config.debriefings:
        lines += [
            f"class {entry.classname.strip()}",
            "{",
            f'\ttitle = "{_esc(entry.title)}";',
            f'\tsubtitle = "{_esc(entry.subtitle)}";',
            f'\tdescription = "{_one_line(_esc(entry.description))}";',
            f'\tpictureBackground = "{entry.picture_background}";',
            "};",
            "",
        ]
    path = Path(mission_dir) / DEBRIEFING
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
