"""Tests for reading the class Intel block out of mission.sqm."""
from pathlib import Path

from arma3_phantom_loader.generators.sqm_intel import IntelValues, parse_intel

FIXTURE = Path(__file__).parent / "fixtures" / "mission_folder"

# The full Intel block the user showed, incl. a negative minute and every
# weather/fog field the tool has a widget for (and wind/waves/lightning it does
# not).
FULL_INTEL = """\
class Mission
{
\tclass Intel
\t{
\t\tresistanceWest=0;
\t\tresistanceEast=1;
\t\ttimeOfChanges=1800.0002;
\t\tstartWeather=0.10484093;
\t\tstartFog=0.011985922;
\t\tstartWind=0.1;
\t\tstartWaves=0.1;
\t\tforecastWeather=0.10175306;
\t\tforecastFog=0.0059227268;
\t\tforecastWind=0.1;
\t\tforecastWaves=0.1;
\t\tforecastLightnings=0.1;
\t\tyear=2026;
\t\tmonth=10;
\t\tday=9;
\t\thour=18;
\t\tminute=-30;
\t\tstartFogBase=1;
\t\tforecastFogBase=1;
\t\tstartFogDecay=0.014;
\t\tforecastFogDecay=0.014;
\t};
};
"""


def _write_mission(tmp_path, text: str) -> str:
    (tmp_path / "mission.sqm").write_text(text, encoding="utf-8")
    return str(tmp_path)


def test_parse_fixture():
    intel = parse_intel(str(FIXTURE))
    assert (intel.year, intel.month, intel.day) == (2035, 7, 6)
    assert (intel.hour, intel.minute) == (8, 42)
    assert intel.time_of_changes == 1800.0002
    assert intel.start_weather == 0.25
    # Fields absent from the fixture stay None.
    assert intel.resistance_west is None
    assert intel.forecast_weather is None
    assert intel.start_fog is None


def test_parse_full_block(tmp_path):
    intel = parse_intel(_write_mission(tmp_path, FULL_INTEL))
    assert intel.resistance_west is False
    assert intel.resistance_east is True
    assert intel.hour == 18
    assert intel.minute == -30  # parser is faithful; normalization happens in UI
    assert intel.start_weather == 0.10484093
    assert intel.start_fog == 0.011985922
    assert intel.forecast_weather == 0.10175306
    assert intel.start_fog_base == 1
    assert intel.start_fog_decay == 0.014
    assert intel.time_of_changes == 1800.0002


def test_wind_waves_lightning_are_not_read(tmp_path):
    intel = parse_intel(_write_mission(tmp_path, FULL_INTEL))
    # No attributes exist for the fields the tool has no widget for.
    assert not hasattr(intel, "start_wind")
    assert not hasattr(intel, "forecast_lightnings")


def test_missing_file_returns_empty(tmp_path):
    assert parse_intel(str(tmp_path)) == IntelValues()


def test_binarized_file_returns_empty(tmp_path):
    (tmp_path / "mission.sqm").write_bytes(b"\0raP\x00\x01binary junk")
    assert parse_intel(str(tmp_path)) == IntelValues()
