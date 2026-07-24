# Arma 3 Phantom Mission Loader 2

A cross-platform (Linux / Windows / macOS) rewrite of
[Arma3PhantomMissionEditorLoader](https://github.com/bennpham/Arma3PhantomMissionEditorLoader)
in Python + PySide6 (Qt).

Point it at a mission folder containing an unbinarized `mission.sqm`, fill in
one tabbed window, hit **Generate Mission Files**, and it sets up the whole
coop mission skeleton in one go:

- Edits `mission.sqm` in place (author, overview, load screen, Coop header,
  respawn templates, Intel date/weather/fog) — the original is backed up to
  `mission.sqm.old`
- Writes `description.ext`, `init.sqf`, `debriefing.hpp`
- Writes `scripts/` (`infotext.sqf`, `briefing.sqf` with FHQ TaskTracker
  briefing + tasks, optional `parameters.hpp`, `briefing_loadout.hpp`,
  `weatherScript.sqf`)
- Installs the SQF functions payload into `functions/`

## What gets installed into `functions/`

| Payload | When |
| --- | --- |
| `fhq_ai`, `fhq_misc`, `fhq_tasktracker` (+ their `.hpp`) | **Always** — all FHQ files are mandatory and included in the generated `common.hpp` |
| `taw_vd` (TAW View Distance) | Only when checked on the Scripts tab |
| `weatherEffects.fsm` | Only when weather effects are checked on the Scripts tab |

The old standalone FHQ folders (forcetracker, markerPatrol, safeAddLoadout,
weatherEffect functions, detectedBy) are consolidated inside `fhq_ai`/`fhq_misc`,
so those features no longer need checkboxes — they are always available
(e.g. `FHQ_fnc_detectedBy`, `FHQ_fnc_forceTrackAdd`, `FHQ_fnc_markerPatrol`,
`FHQ_fnc_safeAddLoadout`). See [SETUP.md](SETUP.md) for their manual setup.

## Install & run

Requires Python 3.9+.

```bash
pip install .
arma3-phantom-loader
```

Or run straight from a checkout without installing:

```bash
pip install PySide6
python3 loader.py            # or: python3 -m arma3_phantom_loader
```

On Linux you may need Qt's runtime libraries, e.g. on Debian/Ubuntu:
`sudo apt install libegl1 libxkbcommon0 libfontconfig1 libdbus-1-3`.

## Usage

1. Create a mission in the Eden editor and save it **unbinarized**
   (the folder should contain just `mission.sqm`).
2. Start the loader and select the mission folder on the **Mission** tab.
3. Work through the tabs — Mission settings, Description & Init, Scripts,
   Debriefing (add at least one entry, e.g. the Win/Lose presets),
   Briefing, and Tasks. On the Tasks tab, pick a **parent task** to turn an
   entry into a subtask — it is shown indented under its parent and written
   to `briefing.sqf` as `["subtask", "parent"]`, after its parent.
4. Click **Generate Mission Files**. Anything that needs manual follow-up
   (ACE gear, player-count scaling, loadouts…) is listed in
   [SETUP.md](SETUP.md).

## Editing the SQF payload without touching the app

The payload is embedded in the package
(`arma3_phantom_loader/payload/functions`), but you can override it:

- put a `functions/` folder (and optionally a `loadscreen.jpg`) next to the
  executable / `loader.py`, or
- set `ARMA3PML_PAYLOAD=/path/to/folder-containing-functions`.

## Building a one-file executable (optional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name Arma3PhantomMissionLoader2 \
  --add-data "arma3_phantom_loader/payload:arma3_phantom_loader/payload" loader.py
```

Run this on each OS you want a binary for (PyInstaller does not
cross-compile). On Windows, replace `:` in `--add-data` with `;`.

## Development

```bash
pip install -e .[dev]
python3 -m pytest        # QT_QPA_PLATFORM=offscreen for headless machines
```

The GUI tabs only fill a `MissionConfig` dataclass
(`arma3_phantom_loader/model.py`); all file generation lives in
`arma3_phantom_loader/generators/` and is covered by the tests without Qt.

## Notes vs. the original loader

- One window with tabs instead of the Form1→7 wizard; everything is written
  in a single Generate pass, and you can review/edit entries before writing.
- Description Params (Player Count Scale) and (FHQ Difficulty) are separate
  checkboxes now.
- The weather script exec line in `init.sqf` is actually written when weather
  effects are enabled (this was silently dropped in the original).
- `mission.sqm` re-generation is idempotent: re-running the loader on an
  already-generated mission does not duplicate keys.

## Credits

- FHQ functions & TaskTracker: Varanon / Alwarren (FHQ)
- TAW View Distance: Tonic
- Convoy functions: Siil
