/*
 * Returns true or false depending on whether all units in _this select 1 are in the
 * trigger in _this select 0
 * 
 * _this select 0: (Object) Trigger name
 * _this select 1: (Array) Units list. If ommited, all playbale units;
 */
 
private ["_res", "_trigger", "_unitsList", "_triggerList", "_auxList"];
    
_trigger = [_this, 0, objNull, [objNull]] call BIS_fnc_param;
_unitsList = [_this, 1, [], [[]]] call BIS_fnc_param;
_playable = (if (isMultiplayer) then {playableUnits} else {switchableUnits});

if (count _unitsList == 0) then {
    _unitsList = _playable;
};

_res = true;

_triggerList = list _trigger;
_auxList = [];

/* First, "resolve" vehicles by adding their crew to the list too */
{
    if (!(_x isKindOf "Man")) then {
        _auxList append (crew _x);
    };
} foreach _triggerList;

if (count _auxList != 0) then {
	_triggerList = _triggerList +  _auxList; // Why does append not work here ? 
};

/* Now, go through the _unitsArray and exit if any of the given units are not in */
{
    if ( alive _x && !(_x in _triggerList)) exitWith {
        _res = false;
    };
} foreach _unitsList;

_res